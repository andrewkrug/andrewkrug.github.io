---           
layout: post
title: How to install Snorby on Ubuntu 10.04
date: 2010-09-01 23:59:48 UTC
updated: 2010-09-01 23:59:48 UTC
comments: false
categories: 
---
Start with a clean install of Ubuntu 10.04 Server. Of course:  

sudo apt-get update && sudo apt-get updgrade -y && sudo reboot (patch)  

Then install the following Debian Packages:  

sudo apt-get install git-core apache2-prefork-dev libapr1-dev libaprutil1-dev libopenssl-ruby ruby ruby1.8-dev rubygems mysql-server apache2  

Install the following packes for ruby using gem to avoid some nasty conflicts:  

sudo gem install prawn  
sudo gem install mysql  
sudo gem install passenger  
sudo gem install -v=2.3.2 rails  

Symlink the Custom gems packages to the bin  

sudo ln -s /var/lib/gems/1.8/bin/pass\* /usr/bin  

Create the database and grant privileges to the snorby user  

mysqladmin -u root -p create snorby  
mysql\> CREATE USER 'snorby'@'localhost' IDENTIFIED BY 'password';  
mysql\> GRANT ALL PRIVILEGES ON snorby.\* TO 'snorby'@'localhost' WITH GRANT OPTION;  

Git Clone Snorby and move it into /var/www and configure the DB and E-Mail Conns.  

git clone git://github.com/mephux/Snorby.git  
sudo mv Snorby/\* /var/www/  

sudo cp /var/www/config/database.yml.example /var/www/config/database.yml  
sudo vim /var/www/config/database.yml  

sudo cp /var/www/config/email.yml.example /var/www/config/email.yml  
sudo vim /var/www/config/email.yml  

sudo cd /var/www/  

Build Snorby  
sudo rake snorby:setup RAILS\_ENV=production  

Install Passenger for Apache  

sudo passenger-install-apache2-module  

sudo vim /etc/apache2/apache2.conf  
Add the following lines:  
LoadModule passenger\_module /var/lib/gems/1.8/gems/passenger-2.2.15/ext/apache2/mod\_passenger.so  
PassengerRoot /var/lib/gems/1.8/gems/passenger-2.2.15  
PassengerRuby /usr/bin/ruby1.8  

Modify the Apache config to support Passenger and Rails applications  

vim /etc/apache2/sites-available/default  
Modify the default site to look like this:  

ServerAdmin webmaster@localhost  
DocumentRoot /var/www/public  

Options FollowSymLinks  
AllowOverride None  

PassengerAppRoot /var/www/  
RailsBaseURI /  
Options Indexes FollowSymLinks  
AllowOverride all  
Options -Multiviews  
Order allow,deny  
allow from all  

Log in to Snorby Web Interface!  

Username: Snorby  
Password: Admin

www.andrewkrug.com E-Mail Comments to andrewkrug@gmail.com