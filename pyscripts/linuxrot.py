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
h11 = net.addDocker( 'h11' ,ip='192.168.10.2/24',mac="00:00:00:00:00:01", dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#h12 = net.addDocker( 'h2' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#h13 = net.addDocker( 'h3' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#h21 = net.addDocker( 'h4' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h22 = net.addDocker( 'h22' ,ip='192.168.20.2/24',mac="00:00:00:00:00:02" , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#h23 = net.addDocker( 'h0' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#hClient = net.addDocker( 'hClient', dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#hServer = net.addDocker( 'hServer' , dimage="ubuntu:trusty", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#volumes=["/:/mnt/vol1:rw"]
#defaultIP1 = '192.168.'  # IP address for r1-eth1
#defaultIP2 = '10.0.3.20/24' # IP address for r2-eth1
r1 = net.addDocker( 'r1', dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"] )
#r2 = net.addDocker( 'r2',dimage="quagga", ip=defaultIP2 )

s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')#,controller=RemoteController,ip=contip)
s2 = net.addSwitch( 's2' ,cls=OVSSwitch, protocols="OpenFlow13")#,controller=RemoteController,ip=contip)


net.addLink( s1, h11 )
#net.addLink( s1, h12 )
#net.addLink( s1, h13 )
#net.addLink( s1, hClient )#, bw=bw)
#net.addLink( s2, hServer)#, bw=bw )
#net.addLink( s2, h21)
net.addLink( s2, h22)
#net.addLink( s2, h23)
net.addLink( s1, r1, intf2='r1-eth0' )
net.addLink( s2, r1, intf2='r1-eth1' )
#net.addLink( s1, s2 )

#net.addLink( s1, r2 )

#net.addLink( s2, r2 )
#net.addLink( r1, r2 )
info('*** Starting network\n')
net.build()

for controller in net.controllers:
    controller.start()
    print(controller,' is available: ',c0.isAvailable())
net.get('s1').start([c0])
net.get('s2').start([c0])




# --------- ROUTER CONFIGURATION -----------
r1.cmd("ifconfig r1-eth0 0")
r1.cmd("ifconfig r1-eth1 0")
# r1.cmd("ifconfig r1-eth0 hw ether 00:00:00:00:01:01")
# r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:01:02")
r1.cmd("ip addr add 192.168.10.1/24 dev r1-eth0") #device
r1.cmd("ip addr add 192.168.20.1/24 dev r1-eth1")
# r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

h11.cmd('route del default gw 172.17.0.1 eth0')
h22.cmd('route del default gw 172.17.0.1 eth0')

h11.cmd("ip route add default via 192.168.10.1")
h22.cmd('ip route add default via 192.168.20.1')

info('*** Testing connectivity\n')
net.pingAll

#time.sleep(5)


#h1.cmd('nohup python3 /root/linkfab4.py '+str(h4.name)+' &')
#h4.cmd('nohup python3 /root/linkfab4.py '+str(h1.name)+' &')

print('*****')
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
