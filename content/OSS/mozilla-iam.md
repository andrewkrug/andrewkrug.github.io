---
title: "Mozilla IAM"
description: "Mozilla Identity and Access Management for Contributors and Staff."
featured_image: images/hero-oss.png
---

[Mozilla IAM Github]('https://github.com/mozilla-iam')

## What is it?

Mozilla’s Identity and Access Management (IAM) aim to improve the productivity of Mozillians (end-users and operational teams) by streamlining IAM management tasks while providing visibility. Additionally, IAM provides an easier and significantly safer experience for the user and for services in need of authentication.

## What did I work on?

The Mozilla Change Integration service and technical architecture for the platform.

Primary repositories include but are not limited to:

- https://github.com/mozilla-iam/sso-dashboard A single signon dashboard flask app that was meant to mimic the Okta login portal.  Eventually configuration for this became stage 1 access.
- https://github.com/mozilla-iam/cis  The Mozilla Change Integration Service.  An event driven system to warehouse and send events for updates to identities.  

## Why is it significant?

The goals of Mozilla's IAM system are unqique in the corporate culture space.  The Vision of the project was to unify the experience for Staff, Contributors, and Contractors to level the playing field.  In addition to this the privacy focus which is baked into the DNA of every Mozilla project allowed Mozillians to choose how they wanted to share attributes about themselves.

All this combined with 1000s of hours of UX research yielded a functional, asthetically pleasing, and usable system that is still in production today.

## What did I learn?

* Making complex systems simple is hard.
* NoSQL databases are not a substitute for good design.
* Team is everything in doing one of these projects.  Scale, scope, and socialization require the highest levels of communication.
* AWS Lambda and Servless provide a nearly maintenance free system with zero downtime.