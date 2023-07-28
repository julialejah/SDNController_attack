# parent image
FROM ubuntu:20.04
# environment variables
ENV TZ=America/Bogota
ENV DEBIAN_FRONTEND=noninteractive  
# install needed packages

# Install OpenJDK-8
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone 
RUN apt-get update && \
    apt-get install -y cron && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant curl unzip && \
    apt-get install -y net-tools && \
    apt-get install -y openssh-server && \
    apt-get install -y --force-yes tshark && \
    apt-get clean; \
    apt-get install -y dbus \
    python3-pip tcpdump\
    && pip3 install setuptools

COPY cicflowmeter.zip /

#RUN chmod 0644 /etc/cron.d/cron
#RUN crontab /etc/cron.d/cron    

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/jre
RUN export JAVA_HOME

# Download ODL 
RUN curl -XGET -O https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.tar.gz
RUN tar -xvzf karaf-0.8.4.tar.gz 

# Copy public key to mypc
RUN mkdir /root/.ssh
RUN echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDRl2ec2E4JZZk7qnw4Q5enmyUHnqyLQo9zJCFR4ukwWl2PwHfabGVirGPAdT/vz3rnalJm+dxtrgrPHQGg+Jj1iKx15rMxtS+c+V+k/vNC8EqyZkiPM2Ltp01VLPfRiugBDrDIlEq7HJ5UvtgKcp7RWWqbTns/IBrrrSN0YmCD05lAXVVpcZOcXAxdrKCZfbOmJsMfsJOKHCGFTQj7J/B2onwNbpupwkb1QDqiWp6tnyKsl+RMNbw+isBhUjnhFDmGWnBqAcHFgirtA2miLyvdnJT233t93rL8G32XWuuLAnMrYwIw6QOhpTFPERfG8QHHfcdMJUXO7243WLOYTId0zgOkjeGKxzLYtKi1YWsDBa8SxTj5E4oIBzOwggEJIRW4YnnW+ZYewNDNpQlKmTKXmjLLgO/VqiemShcu6tSokf7CQT7c7lJL0rSOvD9LJzViGxj0TH+RQUgPOBnMnxcQ6NiuykcZ0Z8nM4s7gyzWhMX/4M/OC68O55W7txK45wk= Julianalejandra@MacBook-Air.local > /root/.ssh/authorized_keys
RUN echo '/etc/init.d/ssh restart' > /etc/rc.local

CMD ["/sbin/init"] 

RUN wget https://inmon.com/products/sFlow-RT/sflow-rt.tar.gz
RUN tar -xvzf sflow-rt.tar.gz
RUN chmod +x /sflow-rt/start.sh

COPY script /root/script
RUN chmod +x /root/script
#RUN /root/script

ENTRYPOINT /root/script && /bin/bash
