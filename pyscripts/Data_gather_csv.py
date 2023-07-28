## Dataset gathering
## Script to create mininet (containernet) for dataset generation
## 4 subnets topology, 5 switches (1 core, 4 access)

from mininet.net import Containernet
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.util import macColonHex
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from scapy.all import *
import time
import random
import pandas as pd
from flowtables.flowtables import get_flow_list
from flowtables.flowtables import call_flow_table
contip = sys.argv[1]
dirhome = sys.argv[2]

setLogLevel('info')
net = Containernet()
c0 = RemoteController (name='C0',controller=RemoteController, 
			port=6653,  ip= contip)

s5 = net.addSwitch('s5', cls=OVSSwitch, protocols='OpenFlow13')
s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
s2 = net.addSwitch('s2', cls=OVSSwitch, protocols='OpenFlow13')
s3 = net.addSwitch('s3', cls=OVSSwitch, protocols='OpenFlow13')
s4 = net.addSwitch('s4', cls=OVSSwitch, protocols='OpenFlow13')

#fc: Flow collector, host that will collect flows using a port mirror in the CORE switch
switches=[s5, s1, s2, s3, s4]
subnet1=[]
subnet2=[]
subnet3=[]
subnet4=[]
fcnet=[]
snlist=[subnet1,subnet2,subnet3,subnet4]
mac = 1
for j in range (5):
    name='fc'+str(j)
    fcnet.append(net.addDocker( name , dimage="cicflows", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root:rw"], cpus="0.5",mac = macColonHex(mac)))
    mac = mac + 1
    net.addLink(switches[j],fcnet[j])
    print(str(switches[j])+' link to '+str(fcnet[j]))

for j in range (3):
    name='s1_h'+str(j)
    subnet1.append(net.addDocker( name , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root:rw"], cpus="0.5",mac = macColonHex(mac)))
    mac = mac + 1
    net.addLink( s1, subnet1[j] )#, bw=bw)
    print('s1 link '+str(subnet1[j]))

for j in range (3):
    name='s2_h'+str(j)
    subnet2.append(net.addDocker( name , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root:rw"], cpus="0.5",mac = macColonHex(mac)))
    mac = mac + 1
    net.addLink( s2, subnet2[j] )
    print('s2 link '+str(subnet2[j]))

for j in range (3):
    name='s3_h'+str(j)
    subnet3.append(net.addDocker( name , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root:rw"], cpus="0.5",mac = macColonHex(mac)))
    mac = mac + 1
    net.addLink( s3, subnet3[j] )
    print('s3 link '+str(subnet3[j]))

for j in range (3):
    name='s4_h'+str(j)
    subnet4.append(net.addDocker( name , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root:rw"], cpus="0.5",mac = macColonHex(mac)))
    mac = mac + 1
    net.addLink( s4, subnet4[j] )
    print('s4 link '+str(subnet4[j]))


net.addLink(s5, s1)
net.addLink(s5, s2)
net.addLink(s5, s3)
net.addLink(s5, s4)
print("inician switches")
#s0.addIntf(Intf(mirr))
for controller in net.controllers:
    controller.start()
    print(controller,' is available: ',c0.isAvailable())

net.get('s5').start([c0])
net.get('s1').start([c0])
net.get('s2').start([c0])
net.get('s3').start([c0])
net.get('s4').start([c0])

net.build()


time.sleep(5)
try:
    flows = call_flow_table(1,contip)
    df = get_flow_list(flows)
    print (df)
    df.to_csv("df1.csv")
    print ("\n")
except:
    print('Error 1')

net.pingAll()


time.sleep(5)

try:
    flows = call_flow_table(1,contip)
    df = get_flow_list(flows)
    print (df)
    df.to_csv("df2.csv")
    print ("\n")
except:
    print('Error 2 ')

for j in range (5):
    switches[j].cmd(
        'ovs-vsctl set bridge '+str(switches[j])+'mirrors=@m --  --id=@p get port eth0 -- --d=@m create mirror name=mir select-all=true output-port=@p'
    )
    print('nuevo port mirror en '+str(switches[j]))
    print(fcnet[j])
    fcnet[j].cmdPrint('touch /root/'+ str(j)+'.pcap')
    fcnet[j].cmdPrint('tshark -i fc'+str(j)+'-eth0 -w /root/'+str(j)+'.pcap &')



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


cont = 0
while (cont < 10):
    print("************* Nueva consulta "+str(cont)+" *************")
    time.sleep(4)
    cont = cont + 1
    df_tot =  pd.DataFrame()
    for i in range (6):
        try:
            print("Tabla "+str(i))
            flows = call_flow_table(i,contip)
            df = get_flow_list(flows)
            df.insert(0, 'Switch', i)  
            df['label'] = 0 
            df_tot = df_tot.append(df) 
           
        except:
            print('Error 3 ')
    print(df_tot)
    df_tot.to_csv('resultado.csv', index=False)

hosts=[subnet1[1],subnet2[1],subnet3[1], subnet4[1]]

time.sleep(30)

for i in hosts:
    i.cmd('python3 /root/rdmac.py '+' '+subnet4[0].IP()+' '+str(10))

cont = 1
while (cont < 10):
    print("************* Nueva consulta attack"+str(cont)+" *************")
    time.sleep(4)
    cont = cont + 1
    df_tot1 =  pd.DataFrame()
    for i in range (6):
        try:
            print("Tabla "+str(i))
            flows = call_flow_table(i,contip)
            df = get_flow_list(flows)
            df.insert(0, 'Switch', i)  
            df['label'] = 1 
            df_tot1 = df_tot1.append(df) 
           
        except:
            print('Error 3 ')
    print(df_tot1)

   

df_tot1.to_csv('resultado1.csv', index=False)


CLI(net)
info('*** Stopping network')
net.stop()
