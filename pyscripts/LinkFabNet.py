## script to test creation of containers in containernet ##
## and the execution of a function for attack in the network ##
## Link fabrication attack and injection of hosts 
## using method in  https://www.mdpi.com/2076-3417/12/3/1103/htm host injection
## using method in Soltani, S., Shojafar, M., Mostafaei, H., Pooranian, Z., & Tafazolli, R. (2021). Link Latency Attack in Software-Defined Networks. Proceedings of the 2021 17th International Conference on Network and Service Management: Smart Management for Future Networks and Services, CNSM 2021, 187–193. https://doi.org/10.23919/CNSM52442.2021.9615598
## ..
## ..
## Args [1] = controller ip 
## Args [2] = repository directory

import requests
import json
import xml.etree.ElementTree as ET
import sys
from mininet.net import Containernet
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.link import OVSLink
from mininet.log import info, setLogLevel
import scapy.all as scapy
import time

contip = sys.argv[1]
dirhome = sys.argv[2]

setLogLevel('info')
net = Containernet(link=TCLink)
c0 = RemoteController (name='C0',controller=RemoteController, 
			port=6653,  ip= contip)
info('*** controller ok \n')
h1 = net.addDocker( 'h1' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h2 = net.addDocker( 'h2' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h3 = net.addDocker( 'h3' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h4 = net.addDocker( 'h4' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h9 = net.addDocker( 'h9' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h0 = net.addDocker( 'h0' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
hClient = net.addDocker( 'hClient', dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
hServer = net.addDocker( 'hServer' , dimage="ubuntu:trusty", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#volumes=["/:/mnt/vol1:rw"]
s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')#,controller=RemoteController,ip=contip)
s2 = net.addSwitch( 's2' ,cls=OVSSwitch, protocols="OpenFlow13")#,controller=RemoteController,ip=contip)
s3 = net.addSwitch( 's3' ,cls=OVSSwitch, protocols="OpenFlow13")#,controller=RemoteController,ip=contip)
#bw=100
s4 = net.addSwitch('s4', cls=OVSSwitch, protocols="OpenFlow13")

#hosts = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h0, hClient]

hosts = [h1, h2, h0, h9, hClient, hServer, h3, h4]

net.addLink( s1, h1 )#, bw=bw)
net.addLink( s1, h2 )#, bw=bw)
net.addLink( s2, h0 )#, bw=bw)
net.addLink( s1, s2)
net.addLink( s2, s3)
#net.addLink( s1, s3)
net.addLink( s1, hClient )#, bw=bw)
net.addLink( s2, hServer)#, bw=bw )
net.addLink( s2, h9)
net.addLink( s3, h3)
net.addLink( s4, h4)
net.addLink( s4, s3)

info('*** Starting network\n')
net.build()
for controller in net.controllers:
    controller.start()
    print(controller,' is available: ',c0.isAvailable())
net.get('s1').start([c0])
net.get('s2').start([c0])
net.get('s3').start([c0])
net.get('s4').start([c0])
print('network started')

h1.cmd('touch /root/h1.pcap')
h1.cmd('nohup tshark -ni h1-eth0 -w /root/h1.pcap  &')
h4.cmd('touch /root/h4.pcap')
h4.cmd('nohup tshark -ni h4-eth0 -w /root/h4.pcap  &')

info('*** Testing connectivity\n')
#for i in hosts:
    #i.cmd('touch /root/net1.pcap')
#    i.cmd('nohup python3 /root/linkfab.py &')
#time.sleep(5)
net.ping(hosts)
print('waiting 10 seconds to start link fabrication attacks from h1 and h2')

time.sleep(10)
h1.cmd('nohup python3 /root/linkfab4.py '+str(h4.name)+' &')
h4.cmd('nohup python3 /root/linkfab4.py '+str(h1.name)+' &')
print('after the LinkFab attack starts, it takes about 10 seconds to reflect in the topology')

print('*****')
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
