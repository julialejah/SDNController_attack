# parent image
FROM ubuntu:20.04

ENV TZ=America/Bogota 
ENV DEBIAN_FRONTEND=noninteractive  

COPY zebra.conf /etc/quagga/
COPY bgpd.conf /etc/quagga/
COPY vtysh.conf /etc/quagga/
COPY debian.conf /etc/quagga/
COPY daemons /etc/quagga/

RUN apt-get update && \
    apt-get install -y quagga && \
    apt-get install -y quagga-doc && \
    apt-get install -y net-tools && \
    apt-get install -y iputils-ping
RUN sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf 
RUN echo 'export VTYSH_PAGER=more' >> /etc/bash.bashrc
RUN chown quagga.quaggavty /etc/quagga/* 
RUN chmod 640 /etc/quagga/*
RUN /etc/init.d/watchquagga restart


