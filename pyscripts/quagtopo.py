## script to test creation of containers in containernet ##
## topology with routers in quagga
## Args [1] = controller ip 
## Args [2] = repository directory

from mininet.net import Containernet
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import sys

# from https://github.com/qyang18/Mininet-Quagga/blob/master/QuaggaOSPF.py


contip =  sys.argv[1]
dirhome = sys.argv[2]

setLogLevel('info') 
net = Containernet(link=TCLink)
c0 = RemoteController (name='C0',controller=RemoteController, 
			port=6653,  ip= contip)
h11 = net.addDocker( 'h11' ,ip='192.168.10.2/24', dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#h12 = net.addDocker( 'h2' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#h13 = net.addDocker( 'h3' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#h21 = net.addDocker( 'h4' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h22 = net.addDocker( 'h22' ,ip='192.168.20.2/24', dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#h23 = net.addDocker( 'h0' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#hClient = net.addDocker( 'hClient', dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#hServer = net.addDocker( 'hServer' , dimage="ubuntu:trusty", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#volumes=["/:/mnt/vol1:rw"]
#defaultIP1 = '192.168.'  # IP address for r1-eth1
#defaultIP2 = '10.0.3.20/24' # IP address for r2-eth1
r1 = net.addDocker( 'r1', dimage="quagga", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"] )
#r2 = net.addDocker( 'r2',dimage="quagga", ip=defaultIP2 )

s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')#,controller=RemoteController,ip=contip)
s2 = net.addSwitch( 's2' ,cls=OVSSwitch, protocols="OpenFlow13")#,controller=RemoteController,ip=contip)


net.addLink( s1, h11 )
net.addLink( s2, h22)
net.addLink( s1, r1, intfName2='r1-eth0' )
net.addLink( s2, r1, intfName2='r1-eth1' )

for controller in net.controllers:
    controller.start()
    print(controller,' is available: ',c0.isAvailable())
net.get('s1').start([c0])
net.get('r1').start()

info('*** Starting network\n')
net.build()

# --------- ROUTER CONFIGURATION -----------
r1.cmd('ifconfig r1-eth0 0')
r1.cmd('ifconfig r1-eth1 0')

r1.setIP(intf='r1-eth0', ip='192.168.10.1/24')
r1.setIP(intf='r1-eth1', ip='192.168.20.1/24')
r1.cmd( 'sysctl net.ipv4.ip_forward=1' )
r1.cmd('ip route add 192.168.10.0/24 via 192.168.10.1')
r1.cmd('ip route add 192.168.20.0/24 via 192.168.20.1')
h11.cmd('ip route add default via 192.168.10.1')
h22.cmd('ip route add default via 192.168.20.1')


# --------- SWITCH CONFIGURATION -----------
#s1.cmd('ovs-ofctl add-flow s1 priority=1,arp,actions=flood')
# print('--------------->'+s1.MAC(intf='s1-eth1'))
# command='ovs-ofctl add-flow s1 priority=65535,ip,dl_dst='+s1.MAC(intf='s1-eth1')+',actions=output:1'
# s1.cmd(command)
# s1.cmd('ovs-ofctl add-flow s1 priority=10,ip,nw_dst=192.168.10.2/24,actions=output:2')

# s2.cmd('ovs-ofctl add-flow s2 priority=1,arp,actions=flood')
# print('--------------->'+s2.MAC(intf='s2-eth2'))
# command='ovs-ofctl add-flow s2 priority=65535,ip,dl_dst='+s2.MAC(intf='s2-eth2')+',actions=output:1'
# s1.cmd(command)
# s1.cmd('ovs-ofctl add-flow s2 priority=10,ip,nw_dst=192.168.20.2/24,actions=output:2')



info('*** Testing connectivity\n')
#net.ping(hosts)


#time.sleep(5)


#h1.cmd('nohup python3 /root/linkfab4.py '+str(h4.name)+' &')
#h4.cmd('nohup python3 /root/linkfab4.py '+str(h1.name)+' &')

print('*****')
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
