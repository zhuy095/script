#!/usr/bin/env python
import sys,time,re,subprocess,os,threading,uuid
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

def get_ip(ip,num):
    ip_new_list=[]
    ip_new_list.append(ip)
    ip_n=ip.split('.')
    print "ip:",ip
    print "ip_n:",ip_n
    for i in range(int(num)-1):
        tmp=ip_n[3]=int(ip_n[3])+1
        if tmp  > 254 :
            ip_n[3]=tmp%254
            ip_n[2]=int(ip_n[2])+int(tmp)/254
            tmp=ip_n[2]
            if tmp > 254 :
                ip_n[2]=int(tmp)%254
                ip_n[1]=int(ip_n[1])+int(tmp)/254
                tmp=ip_n[1]
                if tmp > 254 :
                   ip_n[1]=int(tmp)%254
                   ip_n[0]=int(ip_n[0])+int(tmp)/254
        ip_new_list.append(str(ip_n[0])+"."+str(ip_n[1])+"."+str(ip_n[2])+"."+str(ip_n[3]))
    return ip_new_list

def get_port(port,num):
    ports=[]
    ports.append(port)
    for i in range(int(num)-1):
        ports.append(int(port)+i)
    return ports

def get_send_data(length):
    data=''
    for i in  range(int(length)-42) :
        data+="a"
    return data


def get_mac_address(eth):
    cmd='ifconfig eth1  | grep HWaddr | awk \'{print $5}\''
    pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
    pipe.wait()
    return tcpreplay_pipe.stdout.read()



"""
def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

"""



confs=get_file_value(conf)
print confs
src_eth=find_value("src_eth",confs)
src_ip=find_value("src_ip",confs)
srcip_num=find_value("srcip_num",confs)
src_port=find_value("src_port",confs)
srcport_num=find_value("srcport_num",confs)
dest_eth=find_value("dest_eth",confs)
dest_ip=find_value("dest_ip",confs)
destip_num=find_value("destip_num",confs)
dest_port=find_value("dest_port",confs)
destport_num=find_value("destport_num",confs)
mtu=find_value("mtu",confs)

load=get_send_data(mtu)


print "mtu:",mtu
print "srcip:",src_ip
pcaps=[]
srcips=get_ip(src_ip,srcip_num)
destips=get_ip(dest_ip,destip_num)
srcports=get_port(src_port,srcport_num)
destports=get_port(dest_port,destport_num)
print "srcip:",srcips
print "destip:",destips
print "srcport:",srcports
print "destport:",destports
 
#for i in range(len(srcips)):
#    for j in range(len(destips)):
#        for x in range(len(srcports)):
#            for y in range(len(destports)):

for srcip in srcips:
    for destip in destips:
        for srcport in srcports:
            for destport in destports:
                print "srcip:",srcip
                print "destip:",destip
                print "srcport:",srcport
                print "destport:",destport
                srcport=int(srcport)
                destport=int(destport)
                tmp=str(Ether(dst="aa:bb:cc:dd:ee:ff",src="aa:bb:cc:dd:ee:aa" )/IP(src=srcip,dst=destip)/UDP(sport=srcport,dport=destport)/load)
                pcaps.append(tmp)

s = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,0x0800)
s.bind(('eth1',50007))

for i in range(len(pcaps)):
    s.send(pcaps[i])


"""
a=Ether(dst="aa:bb:cc:dd:ee:ff",src="aa:bb:cc:dd:ee:aa" )/IP(src="192.168.0.1",dst="192.168.0.1")/UDP(sport=1000,dport=1000)/"00000000000000000000"

b=str(a)
s = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,0x0800)
s.bind(('eth1', 50007))
s.send(b)
"""

