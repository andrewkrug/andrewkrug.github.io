---
title: "Datadog HTTP Observatory"
description: "An integration for Datadog to use scan data from the Mozilla HTTP Observatory."
featured_image: images/hero-oss.png
date: "September 7, 2020"
---

[Github]('https://github.com/andrewkrug/datadog-http-observatory')

## What is it?

A scanning integration that consumes a certificate transparency list from [crt.sh]('https://crt.sh') for a given list of domains then scans them with the [Mozilla Web Observatory]('https://observatory.mozilla.org').  The result of the data in the form of A-F scores is then converted to a JSON payload and sent to [Datadog]('https://datadog.com').  

## What did I work on?

I created this integration as part of a blog series on open source and monitoring platforms _like_ Datadog.

## Why is it significant?

This small piece of code demonstrates how easy it can be to create a system that does continuous auditing of an organizations security posture when all systems embrace web standards.  The choice to use AWS Step Functions as well in code makes the scanning system resilient enough to scan **VERY** large orgs as well.

## What did I learn?

* Datadog is easy to develop for.  The documentation is great!  At no point during my iteration could I not find what I was looking for.
* The new AWS Serverless Application Model is easy to use and provides a great scaffold for projects like this.  
* Certificate transparency logs are an incredibly useful tool in studying your organization whether you do or do not have strong governance.