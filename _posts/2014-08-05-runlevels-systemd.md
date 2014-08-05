---
layout: post
title:  "Switching Run Levels in CentOS 7"
date:   2014-08-05 14:23:32
categories: CentOS Linux
---

### Switching Runlevels in CentOS 7

The world has changed and as systemd replaces init it replaces files we have used for years like `/etc/inittab`.

In systemd runlevels have been rebranded as targets.  A target is a group of systemd units that boots.

This table from the [RedHat systemd documentation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/System_Administrators_Guide/sect-Managing_Services_with_systemd-Targets.html) describes the built in targets and their relation to runlevels.



| Runlevel |    Target Units                      | Description |
|----------------------------------------------------------------|
| 0        |  	runlevel0.target, poweroff.target | Shut down and power off the system.|
| 1        |    runlevel1.target, rescue.target   | Set up a rescue shell. |
| 2        |    runlevel2.target, multi-user.target | Set up a non-graphical multi-user system.  |
| 3        | runlevel3.target, multi-user.target |  Set up a non-graphical multi-user system. |
| 4        |  runlevel4.target, multi-user.target | Set up a non-graphical multi-user system. |
| 5        | runlevel5.target, graphical.target |  Set up a graphical multi-user system. |
| 6        | 	runlevel6.target, reboot.target | Shut down and reboot the system. |

> As you can see many of the same runlevel concepts are intact and carried forward.

#### How do I know what  the default runlevel is?

    systemctl get-default

>Shows the default runlevel target.

#### How do I know what runlevels are available?
    systemctl list-units --type target --all

>Shows all the runlevels on the system.  Including custom.

#### How do I know the current runlevel?

    systemctl list-units --type target
>Shows the currently active targets only.


#### How do I change the default runlevel?
    systemctl set-default multi-user.target

#### How do I switch runlevels on the fly?
    systemctl isolate name.target


[jekyll-gh]: https://github.com/jekyll/jekyll
[jekyll]:    http://jekyllrb.com
