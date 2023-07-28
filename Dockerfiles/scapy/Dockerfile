#Dockerfile for a container of a Client host, that could
#act as an attacker to the net (with scapy)

# parent image
FROM ubuntu:bionic
# environment variables
ENV TZ=America/Bogota
ENV DEBIAN_FRONTEND=noninteractive
#ENV DEBIAN_FRONTEND=noninteractive  
# install needed packages
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone &&\
    DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    iproute2 \
    telnet telnetd \
    hping3 \
    iperf \
    tshark \
    python3-pip \
    tcpdump \
    openssh-server \
    && pip3 install scapy \
    && pip3 install pandas \
    && pip3 install Faker 

RUN python3 -m pip install --upgrade pip \
    && pip install paramiko

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN echo 'root:password123' | chpasswd

ENTRYPOINT service ssh restart && bash

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
