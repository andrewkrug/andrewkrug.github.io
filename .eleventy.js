const yaml = require('js-yaml');

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