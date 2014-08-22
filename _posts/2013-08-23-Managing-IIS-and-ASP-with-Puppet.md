---           
layout: post
title: Managing IIS and ASP with Puppet
date: 2013-08-23 21:02:25 UTC
updated: 2013-08-23 21:02:25 UTC
comments: false
categories: 
---
For better or worse our content management system for that my employer uses runs on a Windows Application stack.  C\#, ASP.NET, SQL Server 2012\.  The content management system is SiteCore CMS.   

A current major project is to transfer hosting platforms from a smaller hosting provider to infrastructure as a service on Amazon EC2\.  As part of the transition it seemed to make a lot of sense to consider using configuration management to handle installing, configuring the stack, and deploying the ASP.NET applications associated with running our website.   

I've had the pleasure to write many puppet modules for Linux systems deployment but have never undertaken a puppet on Windows project this substantial before.  

Remembering the basic requirements were:  

* Manage Windows Basic Configuration
  * Firewall
  * Bin Utils
  * Folder Structures

* Manage IIS and Install Desired Features
  * IIS
  * ASP.NET
  * Application Pools
  * .NET Framework Versions

* Deploy my ASP.NET Application 
  * SiteCore CMS Files
  * Manage Database Configuration using .erb templates
  * Spin up IIS

Basically from this I assumed I would need at least 3 modules each with their own set of classes to accomplish what I needed cleanly.  After a lot of research and digging around I found two enormously helpful modules in the puppet forge which I'll talk about a little later in the description of the puppet manifests themselves.  

1. Requirement : Manage Features in Windows
  * Solution : [https://forge.puppetlabs.com/puppetlabs/dism puppetlabs/dism][0] module. The dism module is really great because it lets use create a resource type for installing Features and Roles in Windows.
2. Requirement : Manage IIS Configuration using puppet resources.

  * Solution : [https://forge.puppetlabs.com/simondean/iis][1] .  Puppet IIS gives the user puppet resource types for managing Sites and App\_Pool settings.  This is really incredibly useful because you can automate standard configuration like tearing down "Default Web Site" and Default App Pools from IIS.  Almost every setting that is exposed via appcmd.exe is exposed.  

The first module I decided to create was a base module that just did some things to Windows I like on every server system I work with and do a tiny bit of firewall management.   Not really much here except for the use of a couple execs to add rules to the windows firewall.  See below.  

[![](http://3.bp.blogspot.com/-1VszyaHTjNM/UhfB02893JI/AAAAAAAAEJA/NNH0enQ3qPU/s320/Screen+Shot+2013-08-23+at+1.10.14+PM.png)][2]

The second module I tried to tackle was just a basic installation of IIS with all the requisite features.  Thanks to the inclusion of the puppet forge dism module installing a windows package is as easy as declaring a dism resource type and saying ensure =\> present.  

[![](http://4.bp.blogspot.com/-xz4PAhW0CU0/UhfCugF77TI/AAAAAAAAEJI/ozN2wnrli3k/s320/Screen+Shot+2013-08-23+at+1.14.34+PM.png)][3]

One thing of note about the dism module is that it does not seem to do automatic dependence resolution.  For example if the IIS-Feature IIS-StaticContent requires IIS-WebServerRole the dism module will throw errors the first catalog run and not subsequent runs.  This is easily remedied by chaining together lots of requires statements.  

We all know that exec statements are poor form.  Essentially when you're using puppet if you have to achieve something with an exec you've admitted that puppet doesn't have a resource type that does what you need and you're down to righting hard script.  

I needed the Microsoft .NET Framework 4.5 runtime.  So I simply used a file and a silent install flag to run it to completion as seen below.  

[![](http://4.bp.blogspot.com/-SgdfybAmDqw/UhfDp9-wAzI/AAAAAAAAEJQ/FnXEHiyuKYU/s320/Screen+Shot+2013-08-23+at+1.18.34+PM.png)][4]

Post IIS Configuration it becomes time to prepare IIS for the SiteCore instance that will ultimately run here.  SiteCore is really however no different than any other ASP.NET application.  In my case I decided to break the config, files, app\_pool, and schedule task configuration into their own classes.  

In the init.pp file I simply turned up the services needed to run.  

\`        service { 'W3SVC':

ensure  'running',

enable 'true',

}

service { 'aspnet\_state':

ensure 'running',

enable 'true',

}

\`

The great thing about puppet for windows is that for Windows Services the behavior is nearly the same as linux.  You can even still use notify to trigger a service restart.  

Using the puppet forge iis module you can create or destroy app pools.  Using ensure present and ensure absent I was able to create all the application pools my ASP.NET web app needed and remove the defaults.  

[![](http://3.bp.blogspot.com/-qiLjC2oiaoo/UhfHB8TP4aI/AAAAAAAAEJc/x4pF2u5Y-qo/s320/Screen+Shot+2013-08-23+at+1.31.30+PM.png)][5]

This is where the iis module gets awesome.  If you look at the resource type on https://forge.puppetlabs.com/simondean/iis.  He's exposed almost every single setting that's available in the app pool config.  This includes the ability to do things like disable rapid fail protection by default on your application.  

Rapid fail protection is a thorn in many an admin's side and I personally recommend turning it off by default.  

More on IIS Rapid fail here:

[http://www.iis.net/configreference/system.applicationhost/applicationpools/add/failure][6]

Three resources are needed to create any "Site" in iis.  iis\_site, iis\_app, and iis\_vdir.  Together these all make up the familiar looking Site Objects you know and love.  

[![](http://1.bp.blogspot.com/-iD595xMY45U/UhfIvFtKi2I/AAAAAAAAEJo/2F7uecksv20/s320/Screen+Shot+2013-08-23+at+1.36.15+PM.png)][7]

=

[![](http://2.bp.blogspot.com/-NJFAu-BBiIc/UhfKU1pN5RI/AAAAAAAAEJ0/Nts2xmp4OyE/s1600/Screen+Shot+2013-08-23+at+1.47.06+PM.png)][8]

From there depending on the size of the site you're managing you can use a file resource to populate the files directory.  I had to use a combination of batch files and wget which are pretty gross.  The content I'm loading though is quite large.  Maybe someday when bitsync has a Windows daemon I could use bitsync across all my IIS web servers and manage it with puppet.  

Get these example modules from my GitHub.  They're kind of configuration specific to my app.  But you'll get the idea.

https://github.com/andrewkrug

www.andrewkrug.com E-Mail Comments to andrewkrug@gmail.com

[0]: https://forge.puppetlabs.com/puppetlabs/dism%20puppetlabs/dism
[1]: https://forge.puppetlabs.com/simondean/iis
[2]: http://3.bp.blogspot.com/-1VszyaHTjNM/UhfB02893JI/AAAAAAAAEJA/NNH0enQ3qPU/s1600/Screen+Shot+2013-08-23+at+1.10.14+PM.png
[3]: http://4.bp.blogspot.com/-xz4PAhW0CU0/UhfCugF77TI/AAAAAAAAEJI/ozN2wnrli3k/s1600/Screen+Shot+2013-08-23+at+1.14.34+PM.png
[4]: http://4.bp.blogspot.com/-SgdfybAmDqw/UhfDp9-wAzI/AAAAAAAAEJQ/FnXEHiyuKYU/s1600/Screen+Shot+2013-08-23+at+1.18.34+PM.png
[5]: http://3.bp.blogspot.com/-qiLjC2oiaoo/UhfHB8TP4aI/AAAAAAAAEJc/x4pF2u5Y-qo/s1600/Screen+Shot+2013-08-23+at+1.31.30+PM.png
[6]: http://www.iis.net/configreference/system.applicationhost/applicationpools/add/failure
[7]: http://1.bp.blogspot.com/-iD595xMY45U/UhfIvFtKi2I/AAAAAAAAEJo/2F7uecksv20/s1600/Screen+Shot+2013-08-23+at+1.36.15+PM.png
[8]: http://2.bp.blogspot.com/-NJFAu-BBiIc/UhfKU1pN5RI/AAAAAAAAEJ0/Nts2xmp4OyE/s1600/Screen+Shot+2013-08-23+at+1.47.06+PM.png