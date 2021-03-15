#!/bin/bash

yum install httpd httpd-devel python3 python3-pip python3-devel gcc gcc-c++ mysql-devel git wget unzip make mod_security -y
pip3 install flask flask-mysqldb awscli boto3
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.7.1.zip /tmp/
unzip 4.7.1.zip -d /tmp/
cd /tmp/mod_wsgi-4.7.1/
./configure --with-python=/usr/bin/python3
make && make install
echo "LoadModule wsgi_module modules/mod_wsgi.so" >> /etc/httpd/conf.d/httpd.conf
chkconfig httpd on
cd /tmp/
aws s3 cp s3://nk-ginger-example/app.zip /tmp/
unzip app.zip
mv vuln/ /var/www/
git clone https://github.com/SpiderLabs/owasp-modsecurity-crs.git
cd owasp-modsecurity-crs
cp crs-setup.conf.example /etc/httpd/conf.d/crs-setup.conf
mkdir /etc/httpd/modsecurity.d/
mv rules/ /etc/httpd/modsecurity.d/
rm -rf /etc/httpd/conf.d/mod_security.conf
rm -rf /etc/httpd/conf.d/welcome.conf
aws s3 cp s3://nk-ginger-example/apache-config.conf /etc/httpd/conf/httpd.conf
aws s3 cp s3://nk-ginger-example/mod_security.conf /etc/httpd/modsecurity.d/mod_security.conf