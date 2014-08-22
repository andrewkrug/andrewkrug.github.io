---           
layout: post
title: A Clear and Present Danger
date: 2009-08-03 18:00:06 UTC
updated: 2009-08-03 18:00:06 UTC
comments: false
categories: 
---
[![](http://2.bp.blogspot.com/_CqsRlf7vT4Y/SnclnymtHrI/AAAAAAAAAU0/S47UuDwlil8/s320/Screenshot+on+2009-08-03+at+10.59.07+AM.png)][0]  
So with the Black-hat and Defcon conferences both coming to an end thousands of Security professionals are returning to their desks today in defense mode. There were over 5000 attendees at Defcon this year. Some of them black-hats some of them Security Professionals. But I'm asking myself what does Black-hat and Defcon mean for Southern Oregon University. The hack a day contest reveals a lot of neat new hacks but how many of those effect us? What are the real threats?   

Carefully crafted ICMP packet could crash CAT 6509 Supervisor card. IOS forensics expert from recurity labs states that the right ICMP packet can get you an enable shell on the 6509 if you don't get an enable shell it will DOS the router. Need to configure RANCID (Really Awesome New Cisco confIg Differ) sends a daily report with any changes to the router config. Also need to configure core dump to tftp server on router crash. Otherwise you have no idea why the crash occurred. http://www.shrubbery.net/rancid/  

Metasploit has tons of new zero days for Windows Desktops and out desktop security configuration is no where near where it needs to be. The concept of protection through least privilege computing was discussed in depth. As in not everyone runs as Local Admin. Often time in Defcon many of the researchers are academics so University Faculty are used in many risk models as "the threat". No matter how hard we try to protect our Windows Desktops one faculty member with admin rights could bring it all down by installing some waterfall screensaver with a rootlet. After that an attacker has a foothold inside the network and can escalate to there simply by crawling network drives and skimming metadata from files. Need to run a tools like oometaextractor or get owned by someone using FOCA. There is also an apache mod to strip metadata off documents being served up to the public.  

More on FOCA....  

There was an excellent talk on skimming NEW metadata from files and using that to build an attack dictionary to feed into a password cracker like hydra. So all I really need as an attacker is access to a network drive full of word docs and PDFs, chances are from there I can do enough reconnaissance to own the organization.  

This is just a short list of immediate things to address.

www.andrewkrug.com E-Mail Comments to andrewkrug@gmail.com

[0]: http://2.bp.blogspot.com/_CqsRlf7vT4Y/SnclnymtHrI/AAAAAAAAAU0/S47UuDwlil8/s1600-h/Screenshot+on+2009-08-03+at+10.59.07+AM.png