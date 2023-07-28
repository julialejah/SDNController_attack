## script to test creation of containers in containernet ##
#from mininet.net import Containernet
from mininet.net import Containernet
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.link import OVSLink
from mininet.log import info, setLogLevel

contip='172.17.0.2'

setLogLevel('info')
net = Containernet(link=TCLink)
c0 = RemoteController (name='C0',controller=RemoteController, 
			port=6653,  ip= contip)
info('*** Net created \n')
h1 = net.addHost( 'h1', )
h2 = net.addHost( 'h2' )
h3 = net.addHost( 'h3' )
h4 = net.addHost( 'h4' )
h5 = net.addHost( 'h5' )
h6 = net.addHost( 'h6' )
h7 = net.addHost( 'h7' )
h8 = net.addHost( 'h8' )
h9 = net.addHost( 'h9' )
h0 = net.addHost( 'h0' )
hClient = net.addDocker( 'hClient', dimage="scapy")
hServer = net.addDocker( 'hServer' , dimage="ubuntu:trusty")

s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13',controller=RemoteController,ip=contip)
s2 = net.addSwitch( 's2' ,cls=OVSSwitch, protocols="OpenFlow13",controller=RemoteController,ip=contip)

bw=100

net.addLink( s1, h1 , bw=bw)
net.addLink( s1, h2 , bw=bw)
net.addLink( s1, h3 , bw=bw)
net.addLink( s1, h4 , bw=bw)
net.addLink( s1, h5 , bw=bw)
net.addLink( s2, h6 , bw=bw)
net.addLink( s2, h7 , bw=bw)
net.addLink( s2, h8 , bw=bw)
net.addLink( s2, h9 , bw=bw)
net.addLink( s2, h0 , bw=bw)
net.addLink( s1, s2)
net.addLink( s1, hClient , bw=bw)
net.addLink( s2, hServer, bw=bw )

info('*** Starting network\n')
net.build()
for controller in net.controllers:
    controller.start()
    print(controller,' is available: ',c0.isAvailable())
net.get('s1').start([c0])
net.get('s2').start([c0])
print('network started')


info('*** Testing connectivity\n')
net.ping([hClient, hServer])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
