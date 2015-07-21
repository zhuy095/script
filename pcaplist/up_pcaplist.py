#!/usr/bin/python

import os,commands,thread
import subprocess
import re

def get_file_path(pcap_path):
    pcap_files=[]
    for parent,dirnames,filenames in os.walk(pcap_path):
        for filename in filenames:
            if None!=re.search("pcap$",filename) :
                pcap_files.append(os.path.join(parent,filename))
    return pcap_files


path="pcaps"
pcaps_file='pcaps_list'
update_file='pcap_num'
f=open(pcaps_file,'r')
pcap_from_file=f.readlines()
pcap_from_path=get_file_path(path)
f.close()

f=open(pcaps_file,'a+')
have_file=0
update=0

for i in range(len(pcap_from_file)):
    pcap_from_file[i]=pcap_from_file[i].replace('\n','')

print "pcap_path=",pcap_from_path
print "pcap_path_file=",pcap_from_path



for i in range(len(pcap_from_path)):
    for j in range(len(pcap_from_file)):
        if pcap_from_path[i] == pcap_from_file[j] :
            have_file=0
            break
        else:
            have_file=1

    if have_file == 1:
        f.write(pcap_from_path[i]+"\n")
        update=1
f.close()

if update == 1:
    f=open(update_file,'w')
    t=open(pcaps_file,'r')
    pcaps_file=t.readlines()
    t.close()
    f.write(str(len(pcaps_file)))
    f.close()
