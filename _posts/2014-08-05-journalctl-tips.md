---
layout: post
title:  "JournalCTL Helpful Tips"
date:   2014-08-06 14:30:32
categories: CentOS v7 RedHat Linux Security
---

journalctl replaces syslog daemon. So now ... instead of grepping trough thousands of lines in /var/log/messages you simply can filter the messages and work on them.


#JournalCTL the Evolution of Logging in CentOS

    journalctl

Passed alone without any parameters journalctl opens the systemlog for all targets.

**The coolest thing is probably that journalctl has tab completion for all of the parameters.**

For example journalctl <tab tab> produces the following output

    _AUDIT_LOGINUID=             __MONOTONIC_TIMESTAMP=
    _AUDIT_SESSION=              _PID=
    _BOOT_ID=                    PRIORITY=
    _CMDLINE=                    __REALTIME_TIMESTAMP=
    CODE_FILE=                   _SELINUX_CONTEXT=
    CODE_FUNC=                   _SOURCE_REALTIME_TIMESTAMP=
    CODE_LINE=                   SYSLOG_FACILITY=
    _COMM=                       SYSLOG_IDENTIFIER=
    COREDUMP_EXE=                SYSLOG_PID=
    __CURSOR=                    _SYSTEMD_CGROUP=
    ERRNO=                       _SYSTEMD_OWNER_UID=
    _EXE=                        _SYSTEMD_SESSION=
    _GID=                        _SYSTEMD_UNIT=
    _HOSTNAME=                   _TRANSPORT=
    _KERNEL_DEVICE=              _UDEV_DEVLINK=
    _KERNEL_SUBSYSTEM=           _UDEV_DEVNODE=
    _MACHINE_ID=                 _UDEV_SYSNAME=
    MESSAGE=                     _UID=
    MESSAGE_ID=

This shows all the possible next filters.

>How might I use this you might ask?

To put it simply a million different more useful ways that don't involve pulling awk or cut out of your tool belt.

For example did you know journalctl uses --since as a parameter:

    journalctl _COMM=crond --since "10:00" --until "11:00"

Other common journalctl commands you may want to know:

    journalctl -k

>Shows only dmesg output or "kernel events"