---
layout: post
title:  "Configuring TigerVNC CentOS v7"
date:   2014-08-06 14:23:32
categories: CentOS v7 RedHat Linux Security
---

#VNC Server

#### Install the Requisite Packages

    yum install tigervnc tigervnc-server

#### Create any user accounts that you'll need to use VNC

    $sudo su -
    #useradd larry
    #useradd moe

#### Next Steps

>Quick HowTo:

1. Copy this "/lib/systemd/system/vncserver@.service to /etc/systemd/system/vncserver@:<display>.service"
2. Edit <USER> and vncserver parameters appropriately
     for each user:
    runuser -l <USER> -c /usr/bin/vncserver %i -arg1 -arg2"
3. Run `systemctl daemon-reload`
4. "Run `systemctl enable vncserver@:<display>.service`"

#### Here are the commands I used:

    cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@:1.service

    runuser -l larry -c /usr/bin/vncserver :1
>This prompted for a password

>You will require a password to access your desktops.
Password:


>xauth:  file /home/larry/.Xauthority does not exist
New 'sulu:1 (larry)' desktop is sulu:1
Creating default startup script /home/larry/.vnc/xstartup
Starting applications specified in /home/larry/.vnc/xstartup
Log file is /home/larry/.vnc/sulu:1.log

    systemctl enable vncserver@:1.service

>ln -s '/etc/systemd/system/vncserver@:1.service' '/etc/systemd/system/multi-user.target.wants/vncserver@:1.service'

####Use vinagre binary to test:

1. Connect locally on port 5091
2. Try SSH tunneling on a remote workstation ( Hint use ssh -l)