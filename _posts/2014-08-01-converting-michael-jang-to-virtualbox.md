---
layout: post
title:  "Converting Virtual Machines from KVM to VirtualBox"
date:   2014-08-01 14:23:32
categories: Linux RHCSA KVM VirtualBox
---

#Why

In this case because the Micahel Jang supplemental lab manual for RHCE and RHCSA comes with a disk full of virtual machines in KVM format.  Sometimes you might need those in vbox to run in Windows or OS X.

## Step 1

Install virtual box.  For this step you're mostly on your own.  In my case I opted to install it from the Linux-x64 binary available on the vbox site.

    sudo ./VirtualBox-4.3.14-95030-Linux_amd64.run

## Step 2

Get the vms exported you're interested in converting.  In my case again I'm using the Michael Jang vms from the book RHCSA/ RHCE Red Hat Linux Certification: Exams (Ex200 & Ex300).  I was able to download them from the publishers website.

    [krug@sulu Downloads]$ ls -l
    -rw-------. 1 krug krug 1055186089 Aug  1 14:39 blackhat.tar.gz
    -rw-------. 1 krug krug          0 Aug  1 12:39 gamma.tar.gz
    -rw-------. 1 krug krug 1071997451 Aug  1 14:38 whitehat.tar.gz


## Step 3
I'm going to go ahead and untar one.

    [krug@sulu Downloads]$ tar xzvf whitehat.tar.gz
    tar: Removing leading `/' from member names
    /etc/libvirt/qemu/whitehat.example.net.xml
    /var/lib/libvirt/images/whitehat.example.net.img

> Note the vm's were tarred with the parameter to untar to their original locations.

     [root@sulu Downloads]# cd /var/lib/libvirt/images/
     [root@sulu images]# ls -lh
     total 12G
     -rw-------. 1 root root 12G Sep  9  2012 whitehat.example.net.img


##Step 4
Not quite native vbox.  VirtualBox can run qcow2.  So let's use qemu-img to convert to qcow2.

    > This didn't work at all....
    > qemu-img convert -f raw -O qcow2 whitehat.example.net.img whitehat.qcow2

Second attempt!  Let's use native tools to vbox.

    VBoxManage convertfromraw -format VDI whitehat.example.net.img whitehat.vdi

## Step 5 Modify the permissions

    chmod 754 *.vdi

## Enjoy


