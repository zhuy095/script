#!/usr/bin/env python
import sys,time,re,subprocess,os,multiprocessing,uuid,signal,Queue
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
    run_time=find_value("run_time",confs)
    load=get_send_data(mtu)
    srcips=get_ip(src_ip,srcip_num)
    destips=get_ip(dest_ip,destip_num)
    srcports=get_port(src_port,srcport_num)
    destports=get_port(dest_port,destport_num)
    return srcips,destips,srcports,destports,src_dmac,dest_dmac,src_eth,dest_eth,load,run_time


def get_send_pcaps(srcips,destips,srcports,destports,smac,dmac,load):
    print("\nprepare pcaps,please waiting...")
    print("srcip:%s"%srcips)
    print("destip:%s"%destips)
    print("srcport:%s"%srcports)
    print("destport:%s"%destports)
    pcaps=[]
    for srcip in srcips:
        for destip in destips:
            for srcport in srcports:
                for destport in destports:
                    srcport=int(srcport)
                    destport=int(destport)
                    pcaps.append(str(Ether(dst=dmac,src=smac)/IP(src=srcip,dst=destip)/UDP(sport=srcport,dport=destport)/load))
    print("prepare pcaps complete!")
    return pcaps


def get_socket(eth):
    s = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,0x0800)
    s.bind((eth,50007))
    return s

def send_socket(sfile,pcaps,tims):
    if tims == 0:
        while True:
            for i in range(len(pcaps)):
                sfile.send(pcaps[i])
            if que.empty()==False:
                sfile.close()
                break
    else:
        t=0
        while t<tims:
            for i in range(len(pcaps)):
                sfile.send(pcaps[i])
            t+=1
            if que.empty()==False:
                sfile.close()
                break


def get_arp_pcaps(ips,mac):
    arppcaps=[]
    for ip in ips:
        arp=Ether(dst="ff:ff:ff:ff:ff:ff",src=mac,type=0x0806)/ARP(op=1,hwsrc=mac,psrc=ip,hwdst="00:00:00:00:00:00",pdst=ip)
        arppcaps.append(str(arp))
    return arppcaps

def send_arp(sfile,pcaps):
    for i in range(len(pcaps)):
        sfile.send(pcaps[i])
    time.sleep(30)
    if que.empty()==False:
        send_arp(sfile,pcaps)

def handler(signum,frame):
    que.put("stop")
    cmd='echo 1 > /proc/sys/vm/drop_caches'
    cleanmem_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
    cleanmem_pipe.wait()
    time.sleep(1)
    print("please wait for stop send pcaps")
    print("\n\nstop all......")


try:
    que=Queue.Queue(10) 
    signal.signal(signal.SIGINT, handler)
#    signal.signal(signal.SIGHUP, handler)
#    signal.signal(signal.SIGTERM, handler)
    srcips,destips,srcports,destports,src_dmac,dest_dmac,src_eth,dest_eth,load,run_time=get_send_value()
    
    src_smac=get_mac_address(src_eth)
    src_send_pcaps=get_send_pcaps(srcips,destips,srcports,destports,src_smac,src_dmac,load)
    src_arp_pcaps=get_arp_pcaps(srcips,src_smac)
    
    dest_smac=get_mac_address(dest_eth)
    dest_send_pcaps=get_send_pcaps(destips,srcips,destports,srcports,dest_smac,dest_dmac,load)
    dest_arp_pcaps=get_arp_pcaps(destips,dest_smac)

    pro=[]
    s_file=get_socket(src_eth)
    d_file=get_socket(dest_eth)
    
    
    t=multiprocessing.Process(target=send_arp,args=(s_file,src_arp_pcaps,))
    pro.append(t)
    t=multiprocessing.Process(target=send_arp,args=(d_file,dest_arp_pcaps,))
    pro.append(t)
    t=multiprocessing.Process(target=send_socket,args=(s_file,src_send_pcaps,int(run_time),))
    pro.append(t)
    t=multiprocessing.Process(target=send_socket,args=(s_file,src_send_pcaps,int(run_time),))
    pro.append(t)
#    for i in range(multiprocessing.cpu_count()):
#        if int(i)%2 == 0 :
#            t=multiprocessing.Process(target=send_socket,args=(src_eth,src_send_pcaps,int(run_time),))
#        else:
#            t=multiprocessing.Process(target=send_socket,args=(dest_eth,src_send_pcaps,int(run_time),))
#        pro.append(t)
    
    
    for t in pro:
        t.daemon=False
        t.start()
    #    t.join()
    
    print("\nEnter Ctrl+c to stop...")
    
except:
    handler()
