const yaml = require('js-yaml');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

module.exports = function(eleventyConfig) {
  // Add YAML data file support
  eleventyConfig.addDataExtension("yaml", contents => yaml.load(contents));
  eleventyConfig.addDataExtension("yml", contents => yaml.load(contents));
  
  // Copy static assets
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy("src/CNAME");

  // Current year for the footer copyright
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);
  
  // Watch for changes in CSS
  eleventyConfig.addWatchTarget("src/assets/css/");
  
  // Ignore the images README from being processed as a template
  eleventyConfig.ignores.add("src/images/README.md");

  // Append a content hash to an asset URL, so a changed file is a changed URL.
  // style.css is served with cache-control: max-age=432000 while the HTML gets
  // max-age=600, so without this a returning visitor pairs minutes-old markup with a
  // five-day-old stylesheet, and any new rule that markup depends on is simply absent.
  // A missing file returns the plain URL rather than throwing: a broken link is easier
  // to spot, and much cheaper, than a nightly deploy that cannot build at all.
  eleventyConfig.addFilter("bust", function(url) {
    const clean = String(url).split("?")[0];
    try {
      const bytes = fs.readFileSync(path.join(__dirname, "src", clean));
      return `${clean}?v=${crypto.createHash("sha1").update(bytes).digest("hex").slice(0, 8)}`;
    } catch (e) {
      return clean;
    }
  });

  // Add date comparison filters
  eleventyConfig.addFilter("isPastEvent", function(dateString) {
    const eventDate = new Date(dateString);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return eventDate < today;
  });

  eleventyConfig.addFilter("isFutureEvent", function(dateString) {
    const eventDate = new Date(dateString);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return eventDate >= today;
  });

  // "March 4, 2026" for blog post dates (feed.njk and sitemap.njk still use
  // the raw Date object directly - this filter is only for human-facing
  // text). timeZone: "UTC" matters: a bare "2026-11-01" in front matter
  // parses to midnight UTC, and formatting that in a US build machine's
  // local time prints "October 31" - the day before what's in the file.
  eleventyConfig.addFilter("readableDate", function(dateObj) {
    if (!dateObj) return "";
    return new Date(dateObj).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      timeZone: "UTC",
    });
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts"
    }
  };
};