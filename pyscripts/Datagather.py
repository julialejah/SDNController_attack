## Dataset gathering
## Script to create mininet (containernet) for dataset generation
## 4 subnets topology, 5 switches (1 core, 4 access)
## with 3 attacks 

from mininet.net import Containernet
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.node import Intf
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from scapy.all import *
import time
import random

contip = sys.argv[1]
dirhome = sys.argv[2]

setLogLevel('info')
net = Containernet()
c0 = RemoteController (name='C0',controller=RemoteController, 
			port=6653,  ip= contip)

s0 = net.addSwitch('s0', cls=OVSSwitch, protocols='OpenFlow13')
s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
s2 = net.addSwitch('s2', cls=OVSSwitch, protocols='OpenFlow13')
s3 = net.addSwitch('s3', cls=OVSSwitch, protocols='OpenFlow13')
s4 = net.addSwitch('s4', cls=OVSSwitch, protocols='OpenFlow13')

#fc: Flow collector, host that will collect flows using a port mirror in the CORE switch
switches=[s0, s1, s2, s3, s4]
subnet1=[]
subnet2=[]
subnet3=[]
subnet4=[]
fcnet=[]
snlist=[subnet1,subnet2,subnet3,subnet4]

for j in range (5):
    name='fc'+str(j)
    fcnet.append(net.addDocker( name , dimage="cicflows", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5"))
    net.addLink(switches[j],fcnet[j])
    print(str(switches[j])+' link to '+str(fcnet[j]))

for j in range (3):
    name='s1_h'+str(j)
    subnet1.append(net.addDocker( name , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5"))
    net.addLink( s1, subnet1[j] )#, bw=bw)
    print('s1 link '+str(subnet1[j]))

for j in range (3):
    name='s2_h'+str(j)
    subnet2.append(net.addDocker( name , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5"))
    net.addLink( s2, subnet2[j] )
    print('s2 link '+str(subnet2[j]))

for j in range (3):
    name='s3_h'+str(j)
    subnet3.append(net.addDocker( name , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5"))
    net.addLink( s3, subnet3[j] )
    print('s3 link '+str(subnet3[j]))

for j in range (3):
    name='s4_h'+str(j)
    subnet4.append(net.addDocker( name , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"], cpus="0.5"))
    net.addLink( s4, subnet4[j] )
    print('s4 link '+str(subnet4[j]))


net.addLink(s0, s1)
net.addLink(s0, s2)
net.addLink(s0, s3)
net.addLink(s0, s4)
print("inician switches")
#s0.addIntf(Intf(mirr))
for controller in net.controllers:
    controller.start()
    print(controller,' is available: ',c0.isAvailable())

net.get('s0').start([c0])
net.get('s1').start([c0])
net.get('s2').start([c0])
net.get('s3').start([c0])
net.get('s4').start([c0])

net.build()
net.pingAll()


for j in range (5):
    switches[j].cmd(
        'ovs-vsctl set bridge '+str(switches[j])+'mirrors=@m --  --id=@p get port eth0 -- --d=@m create mirror name=mir select-all=true output-port=@p'
    )
    print('nuevo port mirror en '+str(switches[j]))
    fcnet[j].cmdPrint('touch /root/'+str(j)+'.pcap')
    fcnet[j].cmdPrint('tshark -i fc'+str(j)+'-eth0 -w /root/'+str(j)+'.pcap &')
    print(' inicia captura de paquetes en '+str(fcnet[j])+'! en el archivo /root/'+str(j)+'.pcap')


for i,j,k,l in zip (subnet1, subnet2, subnet3, subnet4):
    i.cmd('service ssh restart')
    j.cmd('service ssh restart')
    k.cmd('service ssh restart')
    l.cmd('service ssh restart')
    i.cmd('python3 /root/normal_user.py '+str(random.choice(subnet2 + subnet3 + subnet4).IP())+' &')
    j.cmd('python3 /root/normal_user.py '+str(random.choice(subnet1 + subnet3 + subnet4).IP())+' &')
    k.cmd('python3 /root/normal_user.py '+str(random.choice(subnet1 + subnet2 + subnet4).IP())+' &')
    l.cmd('python3 /root/normal_user.py '+str(random.choice(subnet1 + subnet2 + subnet3).IP())+' &')
    print('python3 /root/normal_user.py '+str(random.choice(subnet2 + subnet3 + subnet4).IP())+' &')
    print('python3 /root/normal_user.py '+str(random.choice(subnet1 + subnet3 + subnet4).IP())+' &')
    print('python3 /root/normal_user.py '+str(random.choice(subnet1 + subnet2 + subnet4).IP())+' &')
    print('python3 /root/normal_user.py '+str(random.choice(subnet1 + subnet2 + subnet3).IP())+' &')

#s0.cmd('ovs-vsctl set bridge s0 mirrors=@m --  --id=@p get port eth0 -- --d=@m create mirror name=mir select-all=true output-port=@p ')


# info('***start host injection ***\n')

# cont=0
# st=time.time()
# lim=st + 30

# while time.time() < lim:
#     sub=snlist[random.randint(0,3)]
#     sub[random.randint(0,2)].cmd('python3 /root/rdmac.py '+' '+snlist[random.randint(0,3)][random.randint(0,2)].IP()+' '+str(1))
#     cont=cont+1

# print('Los hosts inyectados nuevos son: '+str(cont))

CLI(net)
info('*** Stopping network')
net.stop()