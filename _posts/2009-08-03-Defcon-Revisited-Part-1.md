---           
layout: post
title: Defcon Revisited Part 1
date: 2009-08-03 17:26:12 UTC
updated: 2009-08-03 17:26:12 UTC
comments: false
categories: Defcon 17 2009
---
After 3 days at Defcon I'm feeling a lot of different things the most notable of which are exhaustion, surprise, admiration, and fear. Every year that I come to this conference there are a ton of new topic in security to be cognizant of. This year the scariest things are SSL is broken, no script is hackable, and AES is now less random and much more easily brute forceable than it was before.   

I had always considered SSL (Secure Socket Layer) to be sacred. When all the other things were broken so long as I had good certificates I could trust my information in transit. Well not anymore. According to Dan Kaminsky, "When an attacker who owns his own domain --- badguy.com --- requests a certificate from the CA, the CA, using contact information from Whois records, sends him an email asking to confirm his ownership of the site. But an attacker can also request a certificate for a subdomain of his site, such as Paypal.com\\0.badguy.com, using the null character \\0 in the URL. The CA will issue the certificate for a domain like PayPal.com\\0.badguy.com because the hacker legitimately owns the root domain badguy.com. Then, due to a flaw found in the way SSL is implemented in many browsers, Firefox and others theoretically can be fooled into reading his certificate as if it were one that came from the authentic PayPal site. Basically when these vulnerable browsers check the domain name contained in the attacker's certificate, they stop reading any characters that follow the "\\0 in the name.'"   

Wow right? Most browsers will probably release a patch for this very soon. Since it IS the browsers fault in the way that SSL is implemented.

www.andrewkrug.com E-Mail Comments to andrewkrug@gmail.com