#!/usr/bin/python

import os,commands,ftplib
import subprocess
import re


pcaps_list='pcaps_list'
pcap_num='pcap_num'


def get_ftp_file(filePath):
    f=ftplib.FTP()
    f.connect('192.168.2.105',21,10)
    f.login('anonymous','')
    f.cwd('/replay_pcap')
    print "filePath:",filePath
    filename='RETR '+filePath
    f.retrbinary(filename,open(filePath,'wb').write)
    f.quit()

def update_pcaps():
    r=open(pcap_num,'r')
    r_num=r.readlines()
    r.close()
    get_ftp_file(pcap_num)
    l=open(pcap_num,'r')
    l_num=l.readlines()
    l.close()
    print "r_num",r_num
    print "l_num",l_num
    if int(r_num[0]) != int(l_num[0]) :
        f=open(pcaps_list,'r')
        lpcap_path=f.readlines()
        f.close()
        print "lpcap_path:",lpcap_path
        get_ftp_file(pcaps_list)
        f=open(pcaps_list,'r')
        rpcap_path=f.readlines()
        f.close()
        print "rpcap_path:",rpcap_path
        for i in range(len(rpcap_path)):
            rpcap_path[i]=rpcap_path[i].replace('\n','')
            for j in range(len(lpcap_path)):
                lpcap_path[j]=lpcap_path[j].replace('\n','')
                if rpcap_path[i]==lpcap_path[j]:
                    have_pcap=0
                    break
                else:
                    have_pcap=1
            if int(have_pcap)==int(1):
                print "get pcap:",rpcap_path[i]
                get_ftp_file(rpcap_path[i])
                
update_pcaps()


