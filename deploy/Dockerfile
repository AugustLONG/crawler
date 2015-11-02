FROM ubuntu:12.04
MAINTAINER Feifei Li

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update

ADD adds/supervisord.conf /etc/supervisord.conf

# 容器需要开放HTTP 80端口
EXPOSE 80

# 容器需要开放8080端口
EXPOSE 8080

CMD ["/usr/local/bin/supervisord","-n"]