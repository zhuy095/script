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
    for i in range(1,int(num),1):
        ports.append(int(port)+i)
    return ports

def get_send_data(length):
    data=''
    for i in  range(int(length)-42) :
        data+="a"
    return data


def get_mac_address(eth):
    cmd="ifconfig "+eth+"  | grep HWaddr | awk \'{print $5}\'"
    pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
    pipe.wait()
    return pipe.stdout.read().replace('\n','')

def get_send_value():
    confs=get_file_value(conf)
    src_eth=find_value("src_eth",confs)
    src_ip=find_value("src_ip",confs)
    srcip_num=find_value("srcip_num",confs)
    src_port=find_value("src_port",confs)
    srcport_num=find_value("srcport_num",confs)
    src_dmac=find_value("src_dmac",confs)
    dest_eth=find_value("dest_eth",confs)
    dest_ip=find_value("dest_ip",confs)
    destip_num=find_value("destip_num",confs)
    dest_port=find_value("dest_port",confs)
    destport_num=find_value("destport_num",confs)
    dest_dmac=find_value("dest_dmac",confs)
    mtu=find_value("mtu",confs)
    load=get_send_data(mtu)

    srcips=get_ip(src_ip,srcip_num)
    destips=get_ip(dest_ip,destip_num)
    srcports=get_port(src_port,srcport_num)
    destports=get_port(dest_port,destport_num)
    return srcips,destips,srcports,destports,src_dmac,dest_dmac,src_eth,dest_eth,load


def get_send_pcaps(srcips,destips,srcports,destports,smac,dmac,load):
    print "\nprepare pcaps,please waiting..."
    print "srcip:",srcips
    print "destip:",destips
    print "srcport:",srcports
    print "destport:",destports
    pcaps=[]
    for srcip in srcips:
        for destip in destips:
            for srcport in srcports:
                for destport in destports:
                    srcport=int(srcport)
                    destport=int(destport)
                    pcaps.append(str(Ether(dst=dmac,src=smac)/IP(src=srcip,dst=destip)/UDP(sport=srcport,dport=destport)/load))
    print "prepare pcaps complete!"
    return pcaps


def get_socket(eth):
    s = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,0x0800)
    s.bind((eth,50007))
    return s

def send_socket(sfile,pcaps):
    while True:
        for i in range(len(pcaps)):
            sfile.send(pcaps[i])

    
srcips,destips,srcports,destports,src_dmac,dest_dmac,src_eth,dest_eth,load=get_send_value()

src_smac=get_mac_address(src_eth)
src_send_pcaps=get_send_pcaps(srcips,destips,srcports,destports,src_smac,src_dmac,load)

dest_smac=get_mac_address(dest_eth)
dest_send_pcaps=get_send_pcaps(destips,srcips,destports,srcports,dest_smac,dest_dmac,load)


#sockets=[]
#sockets.append(get_socket(src_eth)
#sockets.append(get_socket(dest_eth)

threads=[]
t1=threading.Thread(target=send_socket,args=(get_socket(src_eth),src_send_pcaps,))
threads.append(t1)
t2=threading.Thread(target=send_socket,args=(get_socket(dest_eth),dest_send_pcaps,))
threads.append(t2)


if __name__=='__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print " all is over"



