# parent image

FROM ubuntu:20.04
ENV TZ=America/Bogota 
ENV DEBIAN_FRONTEND=noninteractive

# install needed packages
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone &&\
    DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
    net-tools \
    unzip \
    iputils-ping \
    iproute2 \
    telnet telnetd \
    hping3 \
    iperf \
    tshark \
    python3-pip \
    tcpdump \
    && pip3 install setuptools

COPY cicflowmeter.zip /
RUN unzip cicflowmeter.zip
WORKDIR /cicflowmeter
RUN python3 setup.py install
WORKDIR /

# run bash interpreter
CMD /bin/bash
