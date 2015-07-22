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

def cap_to_pcap(pcap_path):
    pcap_files=[]
    for parent,dirnames,filenames in os.walk(pcap_path):
        for filename in filenames:
            if None!=re.search("\.cap$",filename) :
                print "cap : ",filename
                pcap_files.append(os.path.join(parent,filename))
    for i in range(len(pcap_files)):
        p=re.compile("cap$")
        pcap=p.sub('pcap',pcap_files[i])
        print "pcap: ",pcap
        cmd="tcpdump -r "+pcap_files[i]+" -w "+pcap
        print "cmd",cmd
        tcp_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
        tcp_pipe.wait() 
        if tcp_pipe.returncode == 0 :
            cmd= "rm -f "+pcap_files[i]
            rm_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
            tcp_pipe.wait()
#        else:
#            print "packet:",pcap_files[i],"  cap to pcap fail!!!!!!!!\n"

path="pcaps"
# cap_to_pcap(path)

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

'''
print "pcap_from_file=",pcap_from_file
print "pcap_from_path=",pcap_from_path
'''
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
