FROM amazonlinux:latest
COPY config.sh /tmp/config.sh
COPY app_files /var/www/vuln/
RUN /tmp/config.sh
COPY apache-config/httpd.conf /etc/httpd/conf/httpd.conf
COPY apache-config/mod_security.conf /etc/httpd/modsecurity.d/mod_security.conf
CMD ["/usr/sbin/httpd", "-DFOREGROUND"]