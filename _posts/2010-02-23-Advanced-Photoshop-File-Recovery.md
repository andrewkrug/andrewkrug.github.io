---           
layout: post
title: Advanced Photoshop File Recovery
date: 2010-02-23 01:48:20 UTC
updated: 2010-02-23 01:48:20 UTC
comments: false
categories: 
---
At Southern Oregon University we offer some 4TB of storage for Art, Music, and Theater to store files. This particular flavor of storage runs on an Apple X Serve backend with an Apple XSAN for the Drive Shelf.   

In this particular instance I was asked to recover 1TB worth of PSD Photoshop Documents from Backup Tape. Because of the volume of Data and lack of robust support by our backup vendor for the OS X platform it took us almost 50 hours to restore the data. Then upon completion of the restore many of the Photoshop Documents ( Multilayered PSDs ) would not open. Photoshop stated, "Could not complete your request because it is not a valid Photoshop Document. IrfanView which usually opens anything was reporting, "Bad File Header or Corrupt Image".   

[![](http://4.bp.blogspot.com/_CqsRlf7vT4Y/S4MF4VId5II/AAAAAAAAAW4/72qxrZtB3so/s400/Screen+shot+2010-02-22+at+2.17.19+PM.png)][0]  
At this point I decided to break out the hex editor to examine the file headers myself. I wanted to examine the files headers or "Magic Numbers". Magic numbers are one way to incorporate metadata, often associated with Unix and its derivatives. Magic numbers are stored inside the file itself. Originally, this term was used for a specific set of 2-byte identifiers at the beginning of a file, but since any undecoded binary sequence can be regarded as a number, any feature of a file format which uniquely distinguishes it can be used for identification. GIF images, for instance, always begin with the ASCII representation of either GIF87a or GIF89a. Photoshop Documents magic number is 8BPS.   

A good Photoshop file is represented like this in a hex editor. Magic number coming first.   

[![](http://1.bp.blogspot.com/_CqsRlf7vT4Y/S4MFNXAyDaI/AAAAAAAAAWo/PxB2jwzsjgA/s400/Good.png)][1]  

The malformed Photoshop documents all had 144 bad blocks on the front, no doubt put there accidentally by the backup system. Perhaps an archive bit or other file flagging feature.   

[![](http://1.bp.blogspot.com/_CqsRlf7vT4Y/S4MFg5IA_XI/AAAAAAAAAWw/Hhn4JCJMqgg/s400/Bad.png)][2]  

At this point I knew the documents could be repaired by simply removing the malformed file header. After succeeding in doing it manually on two files Daniel DeFreez and I decided the best way to clean the files was using Perl and DD. We could read in the file strip off the unneeded 144 blocks and write the file back out as a fully intact Photoshop Document with all the layer metadata intact.   

Below is a copy of the script used to correct the file header problem.   

[![](http://4.bp.blogspot.com/_CqsRlf7vT4Y/S4MIcEkiJmI/AAAAAAAAAXA/es4wm4FulQg/s400/sanitizedscript.png)][3]  

Hopefully this serves as a guide to start from for anyone attempting file recovery of PSDs from a corrupted backup. Before per suing this course of action on our own we had consulted with Adobe, Syncsort BackupExpress (Backup Vendor), and numerous other sources to determine why these were corrupt. At the end of the day though it was simple file header corruption. Too much data instead of not enough.

www.andrewkrug.com E-Mail Comments to andrewkrug@gmail.com

[0]: http://4.bp.blogspot.com/_CqsRlf7vT4Y/S4MF4VId5II/AAAAAAAAAW4/72qxrZtB3so/s1600-h/Screen+shot+2010-02-22+at+2.17.19+PM.png
[1]: http://1.bp.blogspot.com/_CqsRlf7vT4Y/S4MFNXAyDaI/AAAAAAAAAWo/PxB2jwzsjgA/s1600-h/Good.png
[2]: http://1.bp.blogspot.com/_CqsRlf7vT4Y/S4MFg5IA_XI/AAAAAAAAAWw/Hhn4JCJMqgg/s1600-h/Bad.png
[3]: http://4.bp.blogspot.com/_CqsRlf7vT4Y/S4MIcEkiJmI/AAAAAAAAAXA/es4wm4FulQg/s1600-h/sanitizedscript.png