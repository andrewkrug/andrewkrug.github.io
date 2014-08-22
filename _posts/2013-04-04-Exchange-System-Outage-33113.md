---           
layout: post
title: Exchange System Outage 3/31/13
date: 2013-04-04 17:50:59 UTC
updated: 2013-04-04 17:50:59 UTC
comments: false
categories: Systems Outage
---
The week was definitely off to a rough start when I received a call Sunday morning that our e-mail system was failing to deliver mail to a subset of our users.  Microsoft Exchange Administration is not my forte. After trying for 15 minutes to reach our mail system administrator I set to work actually trying to solve the problem.  At the Oregon Shakespeare Festival we have 5 mailbox servers, 1 remote access server, and 1 mail routing server.  Diagnostics showed one mail database has been unmounted due to a lack of free disk space.  I was relieved ... A problem I could solve without having to have intimate knowledge of Exchange.  It took a total of 30-minutes to expand the storage group for the database.  After expansion I rebooted the mailbox and watched as the post office came back online.

www.andrewkrug.com E-Mail Comments to andrewkrug@gmail.com