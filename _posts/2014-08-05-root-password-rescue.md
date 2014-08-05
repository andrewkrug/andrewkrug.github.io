---
layout: post
title:  "Root Password Recovery in CentOS v7"
date:   2014-08-05 14:23:32
categories: CentOS Linux Security
---

#CentOS 7 and Single User Mode

With the changes made to RHEL 7 and CentOS 7 booting into single user mode gets a little bit more complex.

Step 1. From the Grub menu press the "e" key to enter edit mode.

Step 2. Scroll down until you find the line with the "kernel parameters".
    linux16 /vmlinuz-3.10.0-123.4.4.el7.x86_64 root=/dev/mapper/centos-root ro         rd.lvm.lv=centos/swap vconsole.font=latarcyrheb-sun16 rd.lvm.lv=centos/root crashkernel=auto  vconsole.keymap=us rhgb quiet LANG=en_US.UTF-8
    initrd16 /initramfs-3.10.0-123.4.4.el7.x86_64.img
> It should look something like this.

Step 3.  After the language parameter add ` init=/bin/sh `

    linux16 /vmlinuz-3.10.0-123.4.4.el7.x86_64 root=/dev/mapper/centos-root ro       rd.lvm.lv=centos/swap vconsole.font=latarcyrheb-sun16 rd.lvm.lv=centos/root crashkernel=auto  vconsole.keymap=us rhgb quiet LANG=en_US.UTF-8 init=/bin/sh
> It should look something like this

Step 4.  Press the CTRL+X key to proceed with booting.

Step 5.  Now you're in a single user shell.

Step 6.  Remount the file system read and write.  By default it is mounted without write.
    mount -o remount, rw /

Step 7. Run the passwd command and follow the instructions displayed on the command line.
    passwd

Step 8. To make sure that SELinux context of the files that were modified is restored properly after boot, run
    touch /.autorelabel

Step 9. Run the exec /sbin/init command to resume the initialization and finish the system boot.
    exec /sbin/init


## Other Boot Options

#### Single User Mode
    linux16 /vmlinuz-3.10.0-123.4.4.el7.x86_64 root=/dev/mapper/centos-root ro       rd.lvm.lv=centos/swap vconsole.font=latarcyrheb-sun16 rd.lvm.lv=centos/root crashkernel=auto  vconsole.keymap=us rhgb quiet LANG=en_US.UTF-8
        initrd16 /initramfs-3.10.0-123.4.4.el7.x86_64.img -s


#### Emergency Mode
    linux16 /vmlinuz-3.10.0-123.4.4.el7.x86_64 root=/dev/mapper/centos-root ro       rd.lvm.lv=centos/swap vconsole.font=latarcyrheb-sun16 rd.lvm.lv=centos/root crashkernel=auto  vconsole.keymap=us rhgb quiet LANG=en_US.UTF-8
        initrd16 /initramfs-3.10.0-123.4.4.el7.x86_64.img -b


[jekyll-gh]: https://github.com/jekyll/jekyll
[jekyll]:    http://jekyllrb.com
