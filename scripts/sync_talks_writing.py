#!/usr/bin/env python3
"""Pull approved talks/writing from the n8n scraper webhooks into src/_data/, but only
entries that carry every detail the site actually renders.

The scrapers discover candidates; they do not verify them. A discovered entry routinely
arrives with event/location/date empty, type set to the literal "Discovered", a Google
redirect in place of the article URL, or a description that hedges about whether the piece
is even Andrew's. speaking.njk and writing.njk render event, location, date, publication,
title and description WITHOUT any {% if %} guard, so an incomplete entry does not degrade
gracefully: it publishes blank metadata to a live site.

So this script's contract is: an entry is merged only when it is complete and plausible.
Anything else is held back, written to the review file with the exact reason, and never
touched again until a human completes it. Nothing is ever invented to fill a gap.

Usage:
  sync_talks_writing.py                 fetch, validate, merge, build-check, commit, push
  sync_talks_writing.py --dry-run       do everything except write, commit or push
  sync_talks_writing.py --report-only   only say what would be accepted or held back
  sync_talks_writing.py --strict        exit non-zero if anything was held back
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

REPO_DIR = Path(__file__).resolve().parent.parent
TALKS_URL = "https://pickle15.birman-godzilla.ts.net/webhook/andrewkrug-talks"
WRITING_URL = "https://pickle15.birman-godzilla.ts.net/webhook/andrewkrug-writing"
TIMEOUT_SECONDS = 30
REVIEW_PATH = Path.home() / ".andrewkrug-site-sync" / "needs-review.json"

# Fields each template renders with no {% if %} around them: absent or blank means the
# live page shows a hole, so these are hard requirements.
REQUIRED_TALK = ("title", "type", "event", "location", "date", "description")
REQUIRED_WRITING = ("title", "publication", "date", "description", "url")

# Values that look like data but carry no information. "discovered" is the scraper's own
# placeholder for talk type; the rest are the usual human stand-ins.
PLACEHOLDERS = {
    "", "-", "--", "?", "n/a", "na", "none", "null", "nil", "tbd", "tba", "unknown",
    "discovered", "untitled", "no title", "no date", "various", "misc", "other",
}

# A description that hedges is the scraper telling us it could not confirm authorship.
HEDGE_PATTERNS = (
    r"\bmight be\b", r"\bmight have\b", r"\bmay be\b", r"\bpossibly\b", r"\bappears? to be\b",
    r"\bprobably\b", r"\bunclear\b", r"\bnot sure\b", r"\bpresumably\b", r"\bseems to be\b",
    r"\bcould be\b", r"\bor be a general\b", r"\bwhich might\b",
)

# Hosts that hand back a redirect instead of the article. The payload is opaque, so these
# cannot be unwrapped reliably and must not be stored as an article URL.
REDIRECT_HOSTS = (
    "google.com", "www.google.com", "news.google.com", "google.co.uk",
    "bing.com", "www.bing.com", "duckduckgo.com", "r.search.yahoo.com",
    "t.co", "lnkd.in", "l.facebook.com", "out.reddit.com",
)
REDIRECT_PATHS = ("/goto", "/url", "/aclk", "/imgres", "/interstitial")

MIN_DESCRIPTION_CHARS = 40
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


# --------------------------------------------------------------------------- fetching

def fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        print(f"WARN: could not fetch {url}: {exc}")
        return None


# --------------------------------------------------------------------------- validation

def blank(value):
    """True when a value carries no information, including scraper placeholders."""
    if value is None:
        return True
    if isinstance(value, (list, tuple, dict)):
        return len(value) == 0
    return str(value).strip().lower() in PLACEHOLDERS


def url_problem(raw):
    """Why this URL is unusable as a permanent link, or None when it is fine."""
    if blank(raw):
        return "url is empty"
    url = str(raw).strip()
    parts = urllib.parse.urlparse(url)
    if parts.scheme not in ("http", "https"):
        return f"url scheme is {parts.scheme or 'missing'!r}, expected http(s)"
    if not parts.netloc:
        return "url has no host"
    host = parts.netloc.lower().split(":")[0]
    if host in REDIRECT_HOSTS and any(parts.path.startswith(p) for p in REDIRECT_PATHS):
        return (f"url is a {host} redirect ({parts.path}), not the article itself — "
                "the real destination must be resolved before this can be published")
    if host in ("t.co", "lnkd.in", "bit.ly", "tinyurl.com"):
        return f"url is a {host} shortener; store the destination instead"
    return None


# The site prints whatever string is in the data, so a scraped "02/27/2026, 08:00 AM, +0000 UTC"
# would appear on the page exactly like that. These are the machine formats seen from the
# scrapers; anything matching one is rewritten into the house style the existing entries use
# ("May 20, 2026"). This reformats a date, it never invents one.
MACHINE_DATE_FORMATS = (
    "%Y/%m/%d", "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y.%m.%d",
    "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y, %I:%M %p",
)
MONTH_NAME_RE = re.compile(
    r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", re.I)


def normalize_date(raw):
    """("May 20, 2026", None) on success, or (original, reason) when it cannot be trusted."""
    if blank(raw):
        return raw, "date is empty"
    text = str(raw).strip()
    if not YEAR_RE.search(text):
        return text, f"date {text!r} does not contain a 4-digit year"

    # strip trailing timezone noise like ", +0000 UTC" before trying machine formats
    stripped = re.sub(r",?\s*[+-]\d{4}(\s+\w+)?$", "", text).strip()
    for fmt in MACHINE_DATE_FORMATS:
        try:
            parsed = dt.datetime.strptime(stripped, fmt)
        except ValueError:
            continue
        return f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}", None

    # already human: "August 2026", "May 20, 2026" -- leave the author's wording alone
    if MONTH_NAME_RE.search(text):
        return text, None
    return text, (f"date {text!r} has a year but no month this script can read; "
                  "write it as 'May 20, 2026' so the page renders it properly")


def date_problem(raw):
    return normalize_date(raw)[1]


def description_problem(raw):
    if blank(raw):
        return "description is empty"
    text = str(raw).strip()
    if len(text) < MIN_DESCRIPTION_CHARS:
        return f"description is only {len(text)} chars (need {MIN_DESCRIPTION_CHARS})"
    for pattern in HEDGE_PATTERNS:
        m = re.search(pattern, text, re.I)
        if m:
            return (f"description hedges ({m.group(0)!r}) — the scraper could not confirm "
                    "this is Andrew's work, so it needs a human decision")
    return None


def validate(entry, kind):
    """Every reason this entry cannot be published, in the order a human would check them."""
    problems = []
    if not isinstance(entry, dict):
        return [f"entry is {type(entry).__name__}, expected an object"]

    required = REQUIRED_TALK if kind == "talk" else REQUIRED_WRITING
    for field in required:
        if blank(entry.get(field)):
            problems.append(f"{field} is missing or blank")

    if not blank(entry.get("date")):
        p = date_problem(entry["date"])
        if p:
            problems.append(p)
    if not blank(entry.get("description")):
        p = description_problem(entry["description"])
        if p:
            problems.append(p)

    if kind == "writing":
        if not blank(entry.get("url")):
            p = url_problem(entry["url"])
            if p:
                problems.append(p)
    else:
        links = entry.get("links") or []
        if not isinstance(links, list):
            problems.append("links is not a list")
        else:
            for i, link in enumerate(links):
                if not isinstance(link, dict):
                    problems.append(f"links[{i}] is not an object")
                    continue
                if blank(link.get("title")):
                    problems.append(f"links[{i}] has no title")
                p = url_problem(link.get("url"))
                if p:
                    problems.append(f"links[{i}]: {p}")

    tags = entry.get("tags")
    if tags is not None and not isinstance(tags, list):
        problems.append("tags is not a list")

    return problems


def clean(entry):
    """Normalise an accepted entry: trim strings, drop empty tags. No value is invented."""
    out = {}
    for k, v in entry.items():
        if k == "date":
            out[k] = normalize_date(v)[0]
        elif isinstance(v, str):
            out[k] = v.strip()
        elif k == "tags" and isinstance(v, list):
            kept = [str(t).strip() for t in v if not blank(t)]
            if kept:
                out[k] = kept
        elif k == "links" and isinstance(v, list):
            out[k] = [{kk: (vv.strip() if isinstance(vv, str) else vv) for kk, vv in link.items()}
                      for link in v if isinstance(link, dict)]
        else:
            out[k] = v
    return out


# --------------------------------------------------------------------------- identity

def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", str(text or "").lower()).strip()


def canonical_url(raw):
    """Host + path, lowercased, without tracking query or trailing slash: the same article
    linked twice with different utm_* parameters must dedupe to one entry."""
    parts = urllib.parse.urlparse(str(raw or "").strip())
    host = parts.netloc.lower().split(":")[0].removeprefix("www.")
    path = parts.path.rstrip("/")
    keep = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query)
            if k.lower() in ("v", "id", "p")]           # youtube ?v=, cms ?id=/?p=
    query = urllib.parse.urlencode(sorted(keep))
    return f"{host}{path}" + (f"?{query}" if query else "")


def talk_identity(entry):
    """A talk is the same talk when its title and event match. The old script keyed on
    links[0].url, which dropped a second talk at the same event URL and dropped any talk
    with no link at all."""
    return (norm(entry.get("title")), norm(entry.get("event")))


def existing_identities(data, sections, kind):
    ids = set()
    for section in sections:
        for entry in data.get(section) or []:
            if not isinstance(entry, dict):
                continue
            if kind == "talk":
                ids.add(talk_identity(entry))
                for link in entry.get("links") or []:
                    if isinstance(link, dict) and link.get("url"):
                        ids.add(canonical_url(link["url"]))
            else:
                if entry.get("url"):
                    ids.add(canonical_url(entry["url"]))
                ids.add((norm(entry.get("title")), norm(entry.get("publication"))))
    return ids


def incoming_identities(entry, kind):
    if kind == "talk":
        out = {talk_identity(entry)}
        for link in entry.get("links") or []:
            if isinstance(link, dict) and link.get("url"):
                out.add(canonical_url(link["url"]))
        return out
    return {canonical_url(entry.get("url")), (norm(entry.get("title")), norm(entry.get("publication")))}


# --------------------------------------------------------------------------- merging

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_yaml(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=100)


def merge(path, payload, sections, kind, held, dry_run):
    """Merge only complete entries. Returns (number accepted, list of accepted titles)."""
    if not payload:
        return 0, []
    data = load_yaml(path)
    for section in sections:
        data.setdefault(section, [])
    seen = existing_identities(data, sections, kind)
    accepted = []

    for section in sections:
        for entry in payload.get(section) or []:
            title = (entry or {}).get("title") if isinstance(entry, dict) else None
            label = str(title or "<untitled>")[:70]

            problems = validate(entry, kind)
            if problems:
                held.append({"kind": kind, "section": section, "title": label,
                             "reasons": problems, "entry": entry})
                continue

            entry = clean(entry)
            ids = incoming_identities(entry, kind)
            if ids & seen:
                continue                       # already on the site; not an error
            seen |= ids
            data[section].insert(0, entry)
            accepted.append(f"{section}: {label}")

    if accepted and not dry_run:
        save_yaml(path, data)
    return len(accepted), accepted


# --------------------------------------------------------------------------- review file

def write_review(held):
    """Everything held back, with reasons, so a human can complete it by hand. Keyed by
    kind+title so re-running does not pile up duplicates of the same incomplete entry."""
    REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if REVIEW_PATH.exists():
        try:
            for item in json.loads(REVIEW_PATH.read_text()).get("held_back", []):
                existing[f"{item.get('kind')}|{item.get('title')}"] = item
        except (json.JSONDecodeError, OSError):
            existing = {}
    now = dt.datetime.now().isoformat(timespec="seconds")
    for item in held:
        key = f"{item['kind']}|{item['title']}"
        prior = existing.get(key, {})
        item["first_seen"] = prior.get("first_seen", now)
        item["last_seen"] = now
        item["times_seen"] = int(prior.get("times_seen", 0)) + 1
        existing[key] = item
    REVIEW_PATH.write_text(json.dumps(
        {"updated": now, "count": len(existing), "held_back": list(existing.values())},
        indent=2, ensure_ascii=False))


# --------------------------------------------------------------------------- git / build

def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=REPO_DIR, check=check,
                          capture_output=True, text=True)


def current_branch():
    """The branch this checkout is actually on. The old script pushed a hardcoded
    'master', which does not exist in this repository."""
    return git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def site_builds():
    """The merged YAML must still build, or the data lands broken on a live site."""
    r = subprocess.run(["npm", "run", "build"], cwd=REPO_DIR, capture_output=True,
                       text=True, timeout=600)
    return r.returncode == 0, (r.stderr or r.stdout).strip()[-600:]


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="validate and report, but do not write, commit or push")
    ap.add_argument("--report-only", action="store_true",
                    help="only report what would be accepted or held back")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero when any entry was held back")
    args = ap.parse_args()
    dry = args.dry_run or args.report_only

    talks_payload = fetch_json(TALKS_URL)
    writing_payload = fetch_json(WRITING_URL)
    if talks_payload is None and writing_payload is None:
        print("Both webhooks failed; nothing to do.")
        return 1

    held = []
    n_talks, talk_titles = merge(REPO_DIR / "src/_data/speaking.yaml", talks_payload,
                                 ("upcoming_talks", "recent_talks"), "talk", held, dry)
    n_writing, writing_titles = merge(REPO_DIR / "src/_data/writing.yaml", writing_payload,
                                      ("featured_articles", "recent_articles"), "writing", held, dry)

    for line in talk_titles + writing_titles:
        print(f"ACCEPT  {line}")
    for item in held:
        print(f"HOLD    [{item['kind']}] {item['title']}")
        for reason in item["reasons"]:
            print(f"          - {reason}")

    if held:
        if not args.report_only:
            write_review(held)
            print(f"\n{len(held)} entry(ies) held back; details in {REVIEW_PATH}")
        else:
            print(f"\n{len(held)} entry(ies) would be held back")

    if not (n_talks or n_writing):
        print("\nNo new complete entries. Nothing to commit.")
        return 1 if (held and args.strict) else 0
    print(f"\n{n_talks} talk(s) and {n_writing} article(s) are complete and were merged.")

    if dry:
        print("Dry run: not writing, committing or pushing.")
        return 0

    ok, err = site_builds()
    if not ok:
        print(f"ERROR: the site does not build after the merge, reverting:\n{err}")
        git("checkout", "--", "src/_data/speaking.yaml", "src/_data/writing.yaml")
        return 1

    status = git("status", "--porcelain", "src/_data/speaking.yaml", "src/_data/writing.yaml")
    if not status.stdout.strip():
        print("Merge produced no diff. Nothing to commit.")
        return 0

    added = []
    if n_talks:
        added.append("speaking.yaml")
        git("add", "src/_data/speaking.yaml")
    if n_writing:
        added.append("writing.yaml")
        git("add", "src/_data/writing.yaml")

    body = "\n".join(f"- {t}" for t in talk_titles + writing_titles)
    git("commit", "-m", f"sync: pull new talks/writing from n8n scrapers ({', '.join(added)})\n\n"
                        f"Only entries carrying every field the templates render were merged; "
                        f"{len(held)} incomplete entry(ies) held back for review.\n\n{body}")
    branch = current_branch()
    push = git("push", "origin", branch, check=False)
    if push.returncode != 0:
        print(f"ERROR: committed locally but could not push to origin/{branch}: "
              f"{(push.stderr or push.stdout).strip()[:300]}")
        return 1
    print(f"Committed and pushed to origin/{branch}: {', '.join(added)}")
    return 1 if (held and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
