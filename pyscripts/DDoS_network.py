## script to test creation of containers in containernet ##
## and the execution of a function for attack in the network ##
## injection of hosts using method in  https://www.mdpi.com/2076-3417/12/3/1103/htm
## and adapted to OpenDayLight

#from mininet.net import Containernet
from mininet.net import Containernet
import sflow_rt.extras.sflow_mod
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from scapy.all import *
#from packetin import pingen
import time

contip = sys.argv[1]
dirhome = sys.argv[2]
print('***start sflow server **')
command = "nohup ./pyscripts/sflow_rt/start.sh &"

print(command)
os.system(command)


setLogLevel('info')
net = Containernet()
c0 = RemoteController (name='C0',controller=RemoteController, 
			port=6653,  ip= contip)
info('*** Net created \n')
h1 = net.addDocker( 'h1' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
h2 = net.addDocker( 'h2' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
h3 = net.addDocker( 'h3' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
h4 = net.addDocker( 'h4' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
h5 = net.addDocker( 'h5' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
h6 = net.addDocker( 'h6' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
h7 = net.addDocker( 'h7' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
h8 = net.addDocker( 'h8' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
h9 = net.addDocker( 'h9' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
h0 = net.addDocker( 'h0' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
hClient = net.addDocker( 'hClient', dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
hServer = net.addDocker( 'hServer' , dimage="ubuntu:trusty", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5")
#volumes=["/:/mnt/vol1:rw"]
s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
s2 = net.addSwitch( 's2' ,cls=OVSSwitch, protocols="OpenFlow13")

#bw=100

hosts = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h0]
botnet = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h0]

net.addLink( s1, h1 )#, bw=bw)
net.addLink( s1, h2 )#, bw=bw)
net.addLink( s1, h3 )#, bw=bw)
net.addLink( s1, h4 )#, bw=bw)
net.addLink( s1, h5 )#, bw=bw)
net.addLink( s2, h6 )#, bw=bw)
net.addLink( s2, h7 )#, bw=bw)
net.addLink( s2, h8 )#, bw=bw)
net.addLink( s2, h9 )#, bw=bw)
net.addLink( s2, h0 )#, bw=bw)
net.addLink( s1, s2)
net.addLink( s1, hClient )#, bw=bw)
net.addLink( s2, hServer)#, bw=bw )


for controller in net.controllers:
    controller.start()
    print(controller,' is available: ',c0.isAvailable())
net.get('s1').start([c0])
net.get('s2').start([c0])


info('*** Starting network\n')
net.build()

print("***start sFlow script for mininet***")
sflow_rt.extras.sflow_mod.sf(net,contip)

print('network started')

info('*** Testing connectivity\n')
net.ping(hosts)


print('wait for 20 seconds to start DDoS...')
time.sleep(20)
print('starting DDoS...')

for i in botnet:
    print('start script in bot '+str(i))
    i.cmd('nohup python3 /root/packetin_dos.py &')

print('wait for 20 seconds to try a new flow...')
time.sleep(20)
net.ping([hClient,hServer])
#hClient.cmd('python3 /root/packetin.py')
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
