---
title: "ThreatResponse"
description: "Tools for automating incident response in AWS."
featured_image: images/hero-oss.png
---

[ThreatResponse Github]('https://github.com/threatresponse')

## What is it?

The ThreatResponse project was started in 2013 by Andrew Krug and Alex McCormack inspired by AWS Security Geek Beetle Bailey.  The goal was to help customers in the cloud perform complex and automated incident response with zero assumptions about the environment.

Later in the timeline Joel Ferrier became heavily involved as the memory acquisition expert ultimately developing MargaritaShotgun.  

There was also significant investment in the UI, UX, and community from Jeff Parr.

## What did I work on?

As project founder I did the intitial design, facilitated much of the ideation, and wrote lots of python for the first version of AWS_IR and ThreatResponse workstation.

## Why is it significant?

The project delivered some of the first free open source tools for automating forensics in AWS.  Some of them are still reccomended today.  It opened a lot of dialogue in the security space and demonstrated what was really possible using the AWS API.

## What did I learn?

This project ran for a long time and there were a lot of learnings.  The biggest take away though was that it's very difficult to build a "no assumptions" tool that helps increase security posture.  The more you can count on a design pattern like AWS Well Architected the bigger the force multiplier for tool designers.

My focus in particular in this area has moved to things like:

* Better multi account patterns
* Continuous auditing
* Security simulation
* Opinionated automation ( via risk scores and step functions )