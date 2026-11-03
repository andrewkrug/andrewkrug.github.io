---
title: The Bugs Are Damn Near Free. The Fixes Aren't.
date: 2026-11-01T12:00:00
description: AI collapsed the cost of finding and exploiting bugs. The bottleneck moved to validating and fixing them, which means Detection, AppSec, and Cloud Security need to share a queue, not three separate ones.
image: /images/blog/the-bugs-are-damn-near-free/hero.jpg
math: true
---

<p class="post-disclosure">Research for this post was AI-assisted; the argument, analysis, and final edit are my own.</p>

## A Flood of Boring Bugs

PHP2Shell sounds like a drink special. It is not a drink special. On October 17, 2026, someone started exploiting it anyway. The fix didn't ship until October 21, and proof-of-concept code was already circulating twelve hours before the embargo lifted. By the time most teams finished reading the advisory, Cloudflare was counting attack attempts in the millions against roughly 37 million exposed hosts ([Moses, 2026](#ref-moses-2026); [Lakshmanan, 2026](#ref-lakshmanan-2026)). PHP2Shell wasn't a zero-day. It's a preview of how little a four-day patch window is worth once exploitation moves this fast. Good news: none of this calls for panic, just better plumbing.

<img src="/images/blog/the-bugs-are-damn-near-free/img-1-flood-of-bugs.jpg" alt="" width="1376" height="768" style="height: auto;" loading="lazy" />

## Attacker Economics

An attacker runs a campaign when expected value is positive:

$$EV = p(\text{success}) \times \text{value} - \text{cost}$$

<img src="/images/blog/the-bugs-are-damn-near-free/img-2-attacker-economics.jpg" alt="" width="1376" height="768" style="height: auto;" loading="lazy" />

AI has spent the last two years driving that cost term toward zero. Finding a bug, writing an exploit, and turning it into something you can run at scale all got cheaper, and the trend hasn't slowed ([Fang et al., 2024](#ref-fang-2024); [Anthropic, 2026a](#ref-anthropic-2026a); [de Moor, 2026](#ref-de-moor-2026)). That leaves defenders two levers, $p$ and $\text{value}$, owned by three teams that do not share a queue.

On the defender side the same economics show up as cost-to-find:

$$C_{\text{find}} = \frac{S_{\text{disc}} + R \cdot t_{\text{triage}}}{p \cdot R}$$

Discovery spend $S_{\text{disc}}$ is heading toward zero. Report volume $R$ is going up. Precision $p$ is going down. The only term that still costs real money is $t_{\text{triage}}$, the human hours per report ([Stenberg, 2025](#ref-stenberg-2025); [Pesoli et al., 2026](#ref-pesoli-2026)).

The bottleneck moved from finding bugs to validating and fixing them ([Anthropic, 2026b](#ref-anthropic-2026b)).

## Cloud Security Is Now Infrastructure Security

Tim Gonda opened fwd:cloudsec Europe 2026 with "Cloud Security Is Dead. Long Live Infrastructure Security." ([Gonda, 2026](#ref-gonda-2026)). His point is not that cloud controls stopped mattering. At mature organizations the playbook worked: lock down the CI/CD pipeline, watch for misconfigurations, put guardrails in front of mistakes, and auto-remediate what slips through. So the residual risk moved into application code, AI pipelines, and supply chains, and into what he called "the seams of organizational responsibility."

<div class="post-callout">
<p class="post-callout-label">Who is Tim Gonda</p>
<p>Tim Gonda has worked cloud security from every side: building infrastructure, defending it in SOC and Fortune 500 security programs, attacking it as an offensive security director, and now leading cloud security engineering at Datadog, where he co-authored the company's public security playbook. When he says the old playbook is finished, it's not a hot take from the sidelines; it's a verdict from someone who's played all four positions.</p>
</div>

<img src="/images/blog/the-bugs-are-damn-near-free/img-3-infrastructure-security.jpg" alt="" width="1376" height="768" style="height: auto;" loading="lazy" />

The incident record agrees. Storm-0558 started with a signing key in a crash dump. tj-actions started with a bot token. Nx s1ngularity started with three ordinary CI misconfigurations. Salesloft Drift went GitHub account to AWS to customer OAuth tokens. Shai-Hulud rode maintainer identity and publish automation ([Waldman, 2024](#ref-waldman-2024); [Bar et al., 2025](#ref-bar-2025); [Strumpflohner, 2025](#ref-strumpflohner-2025); [Lakshmanan, 2025](#ref-lakshmanan-2025); [Check Point Research, 2025](#ref-check-point-research-2025)). The cloud was the destination every time, never the entry point. Whoever owns identity on the control plane owns the outcome.

That's why access hardening ranks first in the bugonomics ROI analysis I'll publish in the first half of 2027. When the cheapest attack is a stolen token, $p$ and $\text{value}$ are set by infrastructure, not application code ([Mogull & Farris, 2024](#ref-mogull-farris-2024); [Google Cloud, 2025](#ref-google-cloud-2025)).

## If You Can't Check Those Boxes, Cloud Security Isn't Dead for You

Gonda's claim has a precondition. It holds if you've already locked down the pipeline, you catch misconfigurations, your guardrails block instead of just alert, and broken things fix themselves without a ticket. Then, in Gonda's own framing, posture is solved and the risk moves to the seams.

<img src="/images/blog/the-bugs-are-damn-near-free/img-4-cant-check-boxes.jpg" alt="" width="1376" height="768" style="height: auto;" loading="lazy" />

Most organizations are not there, and the numbers that matter are not moving ([Datadog, 2025b](#ref-datadog-2025b)):

| Metric | Value | Trend |
| --- | --- | --- |
| AWS IAM users with an access key older than a year | 59% | unchanged from 2024 |
| IAM keys older than three years | 25% | up from 21% |
| Organizations with any data perimeter | 40% | — |
| SCPs used as a perimeter | 0.6% | — |
| RCPs used as a perimeter | 0.1% | — |
| Regional IMDSv2 default switched on | under 3% | pushes enforcement above 95% wherever it's on |
| EC2 instances overprivileged | 19.4% | flat from 19% |
| Overprivileged third-party roles | 12.2% | up from 10% |

What did move, moved because of a default: new instances enforce IMDSv2, old ones do not, and 83% of S3 buckets sit behind a public access block. Left to the organization, the number stays put. Most cloud breaches still start with a compromised credential ([Tafani-Dereeper, 2025](#ref-tafani-dereeper-2025)).

That's the playbook unfinished, not obsolete. The attacker's cost just dropped. The blast radius of your four-year-old key did not. You don't get to skip to the seams.

> "Cloud security is only dead if you already did the work. If you've got year-old keys and no guardrails, you're not at the funeral. You're the body."
>
> — Andrew Krug

## AI Made It Multi-Incident per Day

"Multi-incident per day" depends on what you count, so say what you count. In-the-wild zero-days have not moved: Google counts 90 for 2025 and a 60 to 100 band for years ([Google Threat Intelligence Group, 2026](#ref-gtig-2026)). That's one every four days, and anyone claiming "a zero-day a day" is using the wrong number.

<img src="/images/blog/the-bugs-are-damn-near-free/img-5-multi-incident.jpg" alt="" width="1376" height="768" style="height: auto;" loading="lazy" />

The honest unit is a CVE with first-known in-the-wild exploitation. VulnCheck counted 884 in 2025, about 2.4 a day, and 495 in the first half of 2026, about 2.7 a day ([VulnCheck, 2026a](#ref-vulncheck-2026a), [2026b](#ref-vulncheck-2026b)). Nearly a third were exploited on or before publication day. CISA KEV catches a fraction of them.

<div class="post-callout">
<p class="post-callout-label">Why "in the wild" matters</p>
<p>CVSS tells you how bad a bug could be in theory. In-the-wild exploitation tells you someone already decided it's worth using, against a real target, today. That's the line between a finding and an incident, and it's the signal EPSS and detection telemetry are built to catch. A severity score can't see it; a sensor can.</p>
</div>

The bigger change is velocity. Mandiant's mean time-to-exploit is now negative seven days, and time from initial access to hand-off fell from eight hours in 2022 to 22 seconds in 2025 ([Mandiant, 2026](#ref-mandiant-2026); [CrowdStrike, 2026](#ref-crowdstrike-2026)). Median time from CVE publication to exploitation dropped from 120 days to 80 in a year ([VulnCheck, 2026b](#ref-vulncheck-2026b)). Two or three exploited CVEs a day is survivable. Two or three a day that are live before the patch exists is not, unless detection does the work patching used to do.

AI isn't producing more zero-days; GTIG didn't attribute a single 2025 zero-day to AI ([Google Threat Intelligence Group, 2026](#ref-gtig-2026)). What it's doing is inflating the denominator. CVE volume went from 25,000 in 2022 to 48,000 in 2025 and is tracking toward 66,000 in 2026 ([Gamblin, 2026a](#ref-gamblin-2026a), [2026b](#ref-gamblin-2026b); [Gamblin & Leverett, 2026](#ref-gamblin-leverett-2026)). Of 1,061 CVEs credited to AI-assisted discovery in the first half of 2026, 14 were exploited, the same rate as everything else ([VulnCheck, 2026b](#ref-vulncheck-2026b)). The firehose feeds the triage problem, and triage is where the economics bite.

**Daily rates by unit, 2025:**

- CVEs published: 132/day
- CVEs with first exploitation evidence: 2.4/day
- KEV additions: 0.67/day
- In-the-wild zero-days: one every 4 days
- Human-triaged malicious packages: 39/day

## The Vulnpocalypse Needs Tighter Loops

Each term in the equation has an owner. AppSec owns $\text{cost}$: exploit prevention and patch velocity. Cloud Security owns $\text{value}$: how little access an attacker gets, how far they can spread from there, and whether the target is even reachable in the first place. Detection owns $p$: it shortens the window and tells everyone what is actually being hit. When AI pushes $\text{cost}$ to zero, the game is $p$ and $\text{value}$, so Detection and Cloud Security set AppSec's priorities, not CVSS.

<img src="/images/blog/the-bugs-are-damn-near-free/img-6-tighter-loops.jpg" alt="" width="1376" height="768" style="height: auto;" loading="lazy" />

About 6% of published CVEs have ever been exploited, and EPSS, built from detection telemetry, catches 93% of actually-exploited CVEs for the same investigation budget that gets CVSS only 37% ([Cyentia Institute, 2024](#ref-cyentia-2024); [Jacobs, 2025](#ref-jacobs-2025)). Only 18% of CVSS-critical findings stay critical once you check whether the system is actually in production and reachable from the internet, and Wiz finds that check removes more than half of high-priority findings ([Datadog, 2025a](#ref-datadog-2025a); [Wiz, 2026b](#ref-wiz-2026b)). 77% of organizations need more than a week to ship a critical patch while time-to-exploit is negative ([Cloud Security Alliance, 2026a](#ref-csa-2026a); [Mandiant, 2026](#ref-mandiant-2026)). Patch SLA cannot close that gap. The loops can.

The loops that are missing:

- **Detection to AppSec:** exploitation status drives patch priority, not CVSS. EPSS already pulls in signals from honeypots, intrusion detection, and endpoint tools. The question is whether your own detections feed your own prioritization.
- **Cloud inventory to AppSec:** a CVE on an unreachable workload with a scoped role is not the same CVE as one on an internet-facing host with a year-old admin key. The 18% number is this loop working.
- **AppSec to Detection:** every accepted finding ships with a detection, not just a ticket. No published source spells this out; it follows from the other three loops working.
- **Shared triage:** validation hours are the scarce resource in the $C_{\text{find}}$ denominator. Three separate triage queues is how an 800 USD validation floor becomes 2,400 USD.

## Feedback

The four levers in the bugonomics model are access hardening, exploit prevention, least privilege, and observability. Stack them and attacker expected value crosses zero. No one of the three teams owns more than two. That's the argument for the feedback loop: not because collaboration is nice, but because the equation doesn't go negative any other way. Share the queue, and the math finally works in your favor for once.

<img src="/images/blog/the-bugs-are-damn-near-free/img-7-feedback.jpg" alt="" width="1376" height="768" style="height: auto;" loading="lazy" />

## Methodology

How the numbers were built, with receipts. Full analysis, data, and notebook land in the first half of 2027. I'd rather ship it right than ship it now.

## References

- <a id="ref-anthropic-2026a"></a>Anthropic. (2026a, April 7). Claude Mythos Preview's cybersecurity capabilities. [anthropic.com/research/mythos-preview](https://www.anthropic.com/research/mythos-preview)
- <a id="ref-anthropic-2026b"></a>Anthropic. (2026b, May 22). Project Glasswing: Initial update. [anthropic.com/research/glasswing-initial-update](https://www.anthropic.com/research/glasswing-initial-update)
- <a id="ref-appenzeller-2024"></a>Appenzeller, G. (2024, November 12). Welcome to LLMflation: LLM inference cost is going down fast. Andreessen Horowitz. [a16z.com/llmflation-llm-inference-cost](https://www.a16z.com/llmflation-llm-inference-cost)
- <a id="ref-bar-2025"></a>Bar, R., Berkovich, S., & Nagli, G. (2025, March 15). GitHub Action tj-actions/changed-files supply chain attack (CVE-2025-30066). Wiz. [wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066](https://www.wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066)
- <a id="ref-ceylan-2026"></a>Ceylan, H. (2026). Closing the intelligence-to-detection gap. Box. [blog.box.com/big-cybersecurity-bets-part-2](https://blog.box.com/big-cybersecurity-bets-part-2)
- <a id="ref-check-point-research-2025"></a>Check Point Research. (2025, November 25). Shai-Hulud 2.0: Inside the second coming of the most aggressive npm supply chain attack of 2025. [blog.checkpoint.com/research/shai-hulud-2-0](https://blog.checkpoint.com/research/shai-hulud-2-0-inside-the-second-coming-the-most-aggressive-npm-supply-chain-attack-of-2025/)
- <a id="ref-csa-2026a"></a>Cloud Security Alliance. (2026a, May 21). The bugpocalypse threshold: AI-accelerated vulnerability discovery and patch capacity (v1.0). [labs.cloudsecurityalliance.org](https://labs.cloudsecurityalliance.org/research/ai-accelerated-vuln-discovery-patch-capacity-whitepaper-v1-0/)
- <a id="ref-csa-2026b"></a>Cloud Security Alliance. (2026b, October 14). CSA research note: XBOW AI Chrome full-chain exploit. [labs.cloudsecurityalliance.org](https://labs.cloudsecurityalliance.org/research/csa-research-note-xbow-ai-chrome-full-chain-20261014-csa-sty/)
- <a id="ref-cortes-2024"></a>Cortes, S. (2024, August 2). Why every modern SOC needs a dedicated vulnerability operations center. TechRadar Pro. [techradar.com](https://www.techradar.com/pro/why-every-modern-soc-needs-a-dedicated-vulnerability-operations-center-voc)
- <a id="ref-cottier-2025"></a>Cottier, B., Snodin, B., Owen, D., & Adamczewski, T. (2025, March 12). LLM inference prices have fallen rapidly but unequally across tasks. Epoch AI. [epoch.ai/data-insights/llm-inference-price-trends](https://epoch.ai/data-insights/llm-inference-price-trends)
- <a id="ref-crowdstrike-2026"></a>CrowdStrike. (2026). 2026 global threat report. [crowdstrike.com/en-us/global-threat-report](https://www.crowdstrike.com/en-us/global-threat-report/)
- <a id="ref-cyentia-2024"></a>Cyentia Institute. (2024, July 15). A visual exploration of exploitation in the wild. FIRST. [cyentia.com/epss](https://cyentia.com/epss/)
- <a id="ref-datadog-2024"></a>Datadog. (2024, October 21). State of cloud security 2024. [datadoghq.com/state-of-cloud-security-2024](https://www.datadoghq.com/state-of-cloud-security-2024/)
- <a id="ref-datadog-2025a"></a>Datadog. (2025a, April 23). Datadog's State of DevSecOps 2025 report finds only 18% of critical vulnerabilities are truly critical [Press release]. [investors.datadoghq.com](https://investors.datadoghq.com/news-releases/news-release-details/datadogs-state-devsecops-2025-report-finds-only-18-critical)
- <a id="ref-datadog-2025b"></a>Datadog. (2025b, October). State of cloud security 2025. [datadoghq.com/state-of-cloud-security](https://www.datadoghq.com/state-of-cloud-security/)
- <a id="ref-datadog-2026"></a>Datadog. (2026, February 26). Datadog's State of DevSecOps 2026 report [Press release]. [datadoghq.com](https://datadoghq.com/about/latest-news/press-releases/datadog-state-of-devsecops-report-2026)
- <a id="ref-datadog-security-labs-2026"></a>Datadog Security Labs. (2026). Malicious software packages dataset [Data set]. GitHub. [github.com/DataDog/malicious-software-packages-dataset](https://github.com/DataDog/malicious-software-packages-dataset)
- <a id="ref-de-moor-2026"></a>de Moor, O. (2026, October 13). XBOW built a Chrome full-chain exploit in six days. XBOW. [xbow.com/blog/xbow-built-a-chrome-full-chain-exploit](https://xbow.com/blog/xbow-built-a-chrome-full-chain-exploit)
- <a id="ref-fang-2024"></a>Fang, R., Bindu, R., Gupta, A., & Kang, D. (2024). LLM agents can autonomously exploit one-day vulnerabilities (arXiv:2404.08144). arXiv. [arxiv.org/abs/2404.08144](https://arxiv.org/abs/2404.08144)
- <a id="ref-frichette-2026"></a>Frichette, N., Spir, & Salem. (2026, October 21). PHP2Shell: Critical vulnerabilities in PHP. Datadog Security Labs. [securitylabs.datadoghq.com](https://securitylabs.datadoghq.com/articles/php2shell-critical-vulnerabilities-in-php/)
- <a id="ref-gamblin-2026a"></a>Gamblin, J. (2026a, January 1). 2025 CVE data review. [jerrygamblin.com](https://jerrygamblin.com/2026/01/01/2025-cve-data-review/)
- <a id="ref-gamblin-2026b"></a>Gamblin, J. (2026b, May). CVE 2026 half-year forecast update. [jgamblin.github.io/FirstForecast](https://jgamblin.github.io/FirstForecast/)
- <a id="ref-gamblin-leverett-2026"></a>Gamblin, J., & Leverett, E. (2026, June 15). Vulnerability forecast update. FIRST. [first.org/blog/20260615-vulnerability-forecast-update](https://www.first.org/blog/20260615-vulnerability-forecast-update)
- <a id="ref-gonda-2026"></a>Gonda, T. (2026, September 8). Cloud security is dead. Long live infrastructure security [Conference presentation]. fwd:cloudsec Europe 2026, London, United Kingdom. [youtube.com/watch?v=DtO0CQKUFA0](https://www.youtube.com/watch?v=DtO0CQKUFA0)
- <a id="ref-google-cloud-2025"></a>Google Cloud. (2025, August 14). Cloud CISO perspectives: New Threat Horizons report details evolving risks and defenses. [cloud.google.com](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-new-threat-horizons-details-evolving-risks-and-defenses/)
- <a id="ref-gtig-2026"></a>Google Threat Intelligence Group. (2026, March 5). A 2025 zero-day exploitation analysis. Google Cloud. [cloud.google.com](https://cloud.google.com/blog/topics/threat-intelligence/2025-zero-day-review/)
- <a id="ref-hanson-2025"></a>Hanson, C. (2025). A candid perspective on the cloud threat landscape [Conference presentation]. fwd:cloudsec Europe 2025. [youtube.com/watch?v=8c3unhWyFGA](https://www.youtube.com/watch?v=8c3unhWyFGA)
- <a id="ref-jacobs-2025"></a>Jacobs, J. (2025, March). Introducing EPSS version 4. Empirical Security. [research.empiricalsecurity.com](https://research.empiricalsecurity.com/research/introducing-epss-version-4)
- <a id="ref-lakshmanan-2025"></a>Lakshmanan, R. (2025, September 8). GitHub account compromise led to Salesloft Drift breach. The Hacker News. [thehackernews.com](https://thehackernews.com/2025/09/github-account-compromise-led-to.html)
- <a id="ref-lakshmanan-2026"></a>Lakshmanan, R. (2026, October 25). PHP2Shell exploitation hits government targets. The Hacker News. [thehackernews.com](https://thehackernews.com/2026/10/php2shell-exploitation-hits-government.html)
- <a id="ref-mandiant-2024"></a>Mandiant. (2024, October 15). How low can you go? An analysis of 2023 time-to-exploit trends. Google Cloud. [cloud.google.com](https://cloud.google.com/blog/topics/threat-intelligence/time-to-exploit-trends-2023)
- <a id="ref-mandiant-2026"></a>Mandiant. (2026, March 23). M-Trends 2026. Google Cloud. [cloud.google.com](https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2026)
- <a id="ref-mitre-ctid-2024"></a>MITRE Center for Threat-Informed Defense. (2024, December 16). Summiting the pyramid: Bring the pain. [ctid.mitre.org](https://ctid.mitre.org/blog/2024/12/16/summiting-the-pyramid-bring-the-pain/)
- <a id="ref-mogull-farris-2024"></a>Mogull, R., & Farris, C. (2024, April 23). The universal cloud threat model for cloud-native security (v1.0). Securosis. [securosis.com](https://www.securosis.com/research/papers/the-universal-cloud-threat-model-for-cloud-native-security/)
- <a id="ref-moses-2026"></a>Moses, C. J. (2026, October 21). Amazon threat intelligence identifies PHP2Shell exploitation prior to public disclosure in MadPot. AWS Security Blog. [aws.amazon.com](https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/)
- <a id="ref-nickels-2025"></a>Nickels, K. (2025, April 4). SANS threat analysis rundown in review: Breaking down March 2025's discussion. SANS Institute. [sans.org](https://www.sans.org/blog/sans-threat-analysis-rundown-in-review-breaking-down-march-2025s-discussion)
- <a id="ref-pesoli-2026"></a>Pesoli, Errico, & Cavallaro. (2026). Demystifying the Mythos or disrupting bugonomics? From zero-day asymmetry to defender remediation throughput (arXiv:2605.24632). arXiv. [arxiv.org/abs/2605.24632](https://arxiv.org/abs/2605.24632)
- <a id="ref-sonatype-2026"></a>Sonatype. (2026). State of the software supply chain 2026: Open source malware. [sonatype.com](https://sonatype.com/state-of-the-software-supply-chain/2026/open-source-malware)
- <a id="ref-stenberg-2025"></a>Stenberg, D. (2025, July 14). Death by a thousand slops. [daniel.haxx.se](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/)
- <a id="ref-stenberg-2026"></a>Stenberg, D. (2026, January 26). The end of the curl bug-bounty. [daniel.haxx.se](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)
- <a id="ref-strumpflohner-2025"></a>Strumpflohner, J. (2025, September 5). s1ngularity postmortem. Nx. [nx.dev/blog/s1ngularity-postmortem](https://nx.dev/blog/s1ngularity-postmortem)
- <a id="ref-tafani-dereeper-2025"></a>Tafani-Dereeper, C. (2025, November 10). Key learnings from the 2025 State of Cloud Security study. Datadog. [datadoghq.com](https://www.datadoghq.com/blog/cloud-security-study-learnings-2025/)
- <a id="ref-traxler-2025"></a>Traxler, K. (2025). Confidence predicts accuracy and other lies about cloud security [Conference presentation]. fwd:cloudsec Europe 2025. [youtube.com/watch?v=CYYT581O67Q](https://www.youtube.com/watch?v=CYYT581O67Q)
- <a id="ref-vulncheck-2026a"></a>VulnCheck. (2026a, January 21). 2026 state of exploitation. [vulncheck.com](https://www.vulncheck.com/blog/state-of-exploitation-2026)
- <a id="ref-vulncheck-2026b"></a>VulnCheck. (2026b, July 28). State of exploitation: 1H 2026. [vulncheck.com](https://www.vulncheck.com/blog/state-of-exploitation-1h-2026)
- <a id="ref-waldman-2024"></a>Waldman, A. (2024, April 3). How Storm-0558 hackers stole an MSA key from Microsoft. TechTarget. [techtarget.com](https://www.techtarget.com/searchsecurity/news/366551281/How-Storm-0558-hackers-stole-an-MSA-key-from-Microsoft)
- <a id="ref-wiz-2025"></a>Wiz. (2025, June 18). Cloud attacks retrospective: Evolving tactics, familiar entry points. [wiz.io/blog/cloud-attack-retrospective-2025](https://wiz.io/blog/cloud-attack-retrospective-2025)
- <a id="ref-wiz-2026a"></a>Wiz. (2026a). Cloud threats retrospective 2026. [wiz.io/reports/cloud-threat-retrospective-2026](https://www.wiz.io/reports/cloud-threat-retrospective-2026)
- <a id="ref-wiz-2026b"></a>Wiz. (2026b, August). The state of cloud risk 2026. [wiz.io/reports/state-of-cloud-risk-2026](https://www.wiz.io/reports/state-of-cloud-risk-2026)
