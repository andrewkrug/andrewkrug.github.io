---           
layout: post
title: The Increasing Demand for Storage
date: 2009-02-07 02:27:34 UTC
updated: 2009-02-07 02:27:34 UTC
comments: false
categories: 
---
[![](http://1.bp.blogspot.com/_CqsRlf7vT4Y/SYzw8g04VrI/AAAAAAAAACs/X9K7yGnOm3I/s320/Picture+1.png)][0]  
Early this morning I recieved a few calls from the Help Desk because one of the Groupwise post offices wasn't working. When I checked it out there were some read error relating to file locks on the Database. After checking a few things out I noticed that the backup from last night was still running and had a lock on the database.   

The backup was running in a perpetual loop because it had run out of available tapes to write the data to. In our current standard backup regimen we load 20 LTO3 800GB tapes into a Quantum Tape Library and that does 1 Full Backup and a nightly incremental. According to the log file last nights backup had used all the remaining tapes. That means that overnight our data had grown at least 800GB.  

A storage audit was in order! I began the storage audit and discovered that out of the 4 Terabytes allocated for Departmental drives and Home Directories (or as we call them F:) drives on our campus about 90 Percent was in use. After doing some reporting I was able to determine that roughly 7 percent of our users are responsible for chewing through 50 percent of our storage. (OUCH)  

Additionally I discovered that our current rate of change is 168GB per month roughly. This means that if no one deletes anything (which they never do) we will be out of storage in about 1 month.  

\*\*Note: In the graph a Hog (or outlier) is defined by one who is greater than two standard deviations from the mean amount of storage used by users. The average lies around 4GB.  
\[FACT\] The entire library of congress digitized is 3 Terabytes. \[FACT\]

www.andrewkrug.com E-Mail Comments to andrewkrug@gmail.com

[0]: http://1.bp.blogspot.com/_CqsRlf7vT4Y/SYzw8g04VrI/AAAAAAAAACs/X9K7yGnOm3I/s1600-h/Picture+1.png