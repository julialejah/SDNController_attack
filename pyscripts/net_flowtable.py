## script to test creation of containers in containernet ##

from mininet.net import Containernet
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from scapy.all import *
import time
import requests
import pandas as pd
import sflow_rt.extras.sflow_mod


def get_flow_list(result):
    cols = ["id", "pri", "tb_id","inport","src_mac","dst_mac","eth_type","src_ip","dst_ip","dur-sec","dur-nan", "pkt", "byte" ]
    flow_list = pd.DataFrame(columns=cols)
    list1 = result.get("flow-node-inventory:table")
    fls = list1[0]
    dicfl = fls.get("flow")
    if dicfl is None:
        return 
    for i in range(len(dicfl)):
        #---get data from statistics dictionary
        stats = dicfl[i].get("opendaylight-flow-statistics:flow-statistics")
        pkt_count = stats.get("packet-count")
        byte_count = stats.get("byte-count")
        nanosec = stats.get("duration").get("nanosecond")
        sec = stats.get("duration").get("second")
        #---get data from match dictionary
        inport = "-"
        src_mac = "-" 
        dst_mac = "-"
        dst_ip = "-"
        src_ip = "-"
        eth_type = "-"
        match = dicfl[i].get("match")
        for key,value in match.items():
            if (key == "in-port"):
                inport = value
            elif (key == "ethernet-match"):
                for ethk, ethv in value.items():
                    if (ethk == "ethernet-type"):
                        eth_type = ethv.get("type")
                    elif (ethk == "ethernet-source"):
                        src_mac = ethv.get("address")
                    elif (ethk == "ethernet-destination"):
                        dst_mac = ethv.get("address")
            elif (key == "ipv4-destination"):
                dst_ip = value
            elif (key == "ipv4-source"):
                src_ip = value

        data=[dicfl[i].get("id"),dicfl[i].get("priority"),\
            dicfl[i].get("table_id"),\
                inport, src_mac, dst_mac, eth_type,src_ip, dst_ip, \
                    sec,nanosec,pkt_count,byte_count]
        fl = pd.DataFrame([data],columns=cols)
        flow_list = flow_list.append(fl, ignore_index=True)    
    return flow_list

def call_flow_table(switch):
    url = "http://"+contip+":8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:"+str(switch)+"/table/0"
    headers = {"Content-Type": "application/json"}
    auth = ("admin", "admin")
    respuesta = requests.request(method="GET", url= url, headers=headers, auth=auth)
    flows= respuesta.json()
    return flows


def start_sflow():
    print('***start sflow server **')
    command = "nohup ./pyscripts/sflow_rt/start.sh &"
    print(command)
    os.system(command)
    print("***start sFlow script for mininet***")
    sflow_rt.extras.sflow_mod.sf(net,contip)


contip = sys.argv[1]
dirhome = sys.argv[2]
setLogLevel('info')
#fin




net = Containernet(link=TCLink)
c0 = RemoteController (name='C0',controller=RemoteController, 
			port=6653,  ip= '172.17.0.1')
info('*** Net created \n')
h1 = net.addDocker( 'h1' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h2 = net.addDocker( 'h2' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h3 = net.addDocker( 'h3' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h4 = net.addDocker( 'h4' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h5 = net.addDocker( 'h5' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h6 = net.addDocker( 'h6' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h7 = net.addDocker( 'h7' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h8 = net.addDocker( 'h8' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h9 = net.addDocker( 'h9' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
h0 = net.addDocker( 'h0' , dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
hClient = net.addDocker( 'hClient', dimage="scapy", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
hServer = net.addDocker( 'hServer' , dimage="ubuntu:trusty", volumes=[dirhome+"/SDN_attacks/pyscripts/attacks:/root/:rw"])
#volumes=["/:/mnt/vol1:rw"]
s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
s2 = net.addSwitch( 's2' ,cls=OVSSwitch, protocols="OpenFlow13")

#bw=100

#hosts = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h0, hClient]
hosts = [h1,h9]

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

info('*** Starting network\n')
net.build()
for controller in net.controllers:
    controller.start()
    print(controller,' is available: ',c0.isAvailable())
net.get('s1').start([c0])
net.get('s2').start([c0])

start_sflow()

print('network started')

info('*** Waiting to test connectivity\n')


flows = call_flow_table(1)
df = get_flow_list(flows)
print (df)
print ("\n")

net.pingAll()
flows= call_flow_table(1)
df = get_flow_list(flows)
print (df)
print ("\n")

time.sleep(5)
flows= call_flow_table(1)
df = get_flow_list(flows)

print (df)
print ("\n")

time.sleep(10)

flows= call_flow_table(1)
df = get_flow_list(flows)
print (df)
print ("\n")

info('***start randmac***\n')
print (h2.MAC())
print(h2.IP())
for i in hosts:
    i.cmd('python3 /root/rdmac.py '+' '+h2.IP()+' '+str(10))

try:
    df = get_flow_list(flows)
    print (df)
    print ("\n")
except Exception as e:
    print ("error -- "+ str(e))
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
