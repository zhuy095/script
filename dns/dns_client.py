#!/usr/bin/env python
import sys,time,re,subprocess,os,threading,uuid,signal
from scapy.all import *

pcap=str(Ether(dst="00:0c:29:b4:08:cc",src="00:0c:29:b8:0c:ea")/IP(src="172.16.30.20",dst="172.16.30.220")/UDP()/DNS(ra=1,qdcount=1)/DNSQR(qname="www.123.com",qtype="A",qclass="IN"))


#pcap=str(Ether(dst="00:0c:29:b4:08:cc",src="00:0c:29:b8:0c:ea")/IP(src="172.16.30.20",dst="172.16.30.220")/UDP(dport='53')/DNS(qdcount="1")/DNSQR(qname="www.123.com",qtype="A",qclass="IN"))
s= socket.socket(socket.AF_PACKET,socket.SOCK_RAW,0x0800)
s.bind(("eth1",50007))
for i in range(100):
	s.send(pcap)
s.close

