#!/usr/bin/env python
import sys,time,re,subprocess,os,threading,uuid,signal
from scapy.all import *

address=("172.16.50.10",53)
t=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #可被复用的
t.bind(address)

while 1:
    data,addr=t.recvfrom(2048)
    dnsid=DNS(data).id
    hosts=DNS(data).qd.qname
    hostip="172.16.50.10"
    senddata=str(DNS(id=dnsid,qr=1,rd=1,ra=1,ancount=1,qdcount=1)/DNSQR(qname=hosts,qtype="A",qclass="IN")/DNSRR(rrname=hosts,ttl=86400,rdata=hostip))
    time.sleep(2)
    t.sendto(senddata,addr)
    print "dns send ",addr
t.close

