FROM amazonlinux:latest
COPY config.sh /tmp/config.sh
COPY app_files /var/www/vuln/
RUN /tmp/config.sh
CMD ["/usr/sbin/httpd", "-DFOREGROUND"]