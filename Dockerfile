FROM amazonlinux:latest
COPY config.sh /tmp/config.sh
RUN /tmp/config.sh
CMD ["/usr/sbin/httpd", "-DFOREGROUND"]