---
layout: post
title:  "Key Based Authentication"
date:   2014-08-05 14:23:32
categories: CentOS RedHat Linux Security
---

##CONFIGURING OPENSSH FOR KEY-BASED AUTHENTICATION

In order to ensure key based authentication one must first disable password authentication. To disable password authentication **edit /etc/ssh/sshd_config** in your favorite text editor such as vim.
Change the PasswordAuthentication variable to no
PasswordAuthetication no

>Note: Make sure that PubkeyAuthentication no has not been set and that if you’re connected remotely that you do not disable password authentication until you have verified key based authentication is working. Otherwise you can lock yourself out of the remote system.

##GENERATING KEY PAIRS

Now key pairs must be generated for each user. RHEL 7 uses RSA key pairs by default. Keys are unique to the user who creates them, so if you’re logged in as root and generate a key pair, only the root user will be able to use that key pair.

__1.Generate a key pair:__

    ~]$ ssh-keygen -t rsa

>Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa):

Press ENTER to select the default directory for the generated key.

Now enter a passphrase when prompted. Observe security best practices by using a different passphrase than that of your login to your user account.

After entering your passphrase you’ll see some confirmation text of where your identification has been stored as well as where your public key is.

Now change the permissions of the ~/.ssh/ directory

    ~]$ chmod 700 ~/.ssh

Next, copy the key to the remote machine

    ssh-copy-id user@hostname

>This command will copy all public keys to the remote machine.
