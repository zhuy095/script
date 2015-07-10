#!/usr/bin/env python
import sys,time,re,subprocess,os,threading
from scapy.all import *

conf='udp.conf'

def get_file_value(conf):
    new_conf=[]
    f=open(conf,'r')
    conf=f.readlines()
    f.close()
    for i in range(len(conf)):
        if None!=re.match('.*=.*',conf[i]):
            new_conf.append(conf[i])
    return new_conf

def find_value(key,new_conf):
    for i in range(len(new_conf)):
        p=re.compile(key)
        if None!=p.match(new_conf[i]):
            a=new_conf[i].split('=')
    return a[1].replace('\n','')

confs=get_file_value(conf)

srcip=find_value("srcip",confs)
srcip_num=find_value("srcip_num",confs)
srcport=find_value("srcport",confs)
srcport_num=find_value("srcport_num",confs)
destip=find_value("destip",confs)
destip_num=find_value("destip_num",confs)
destport=find_value("destport",confs)
destport_num=find_value("destport_num",confs)
mtu=find_value("mtu",confs)

print "mtu:",mtu

"""
a=Ether(dst="aa:bb:cc:dd:ee:ff",src="aa:bb:cc:dd:ee:aa" )/IP(src="192.168.0.1",dst="192.168.0.1")/UDP(sport=1000,dport=1000)/"00000000000000000000"

b=str(a)
s = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,0x0800)
s.bind(('eth1', 50007))
s.send(b)
"""

