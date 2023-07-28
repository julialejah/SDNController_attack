## script to test creation of containers in containernet ##
#1

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
    cols = ["id", "pri", "tb_id","inport","src_mac","dst_mac","eth_type","src_ip","dst_ip","dur-sec","pkt", "byte" ]
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
                    sec,pkt_count,byte_count]
        fl = pd.DataFrame([data],columns=cols)
        flow_list = flow_list.append(fl, ignore_index=True)    
    return flow_list

def call_flow_table(switch,contip):
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


#fin