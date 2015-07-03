#!/usr/bin/python

import os,commands
import subprocess
import re
path="pcaps"
f=open('replay.conf','r')
conf=f.readlines()
f.close()


new_conf=[]
for i in range(len(conf)):
    if None!=re.match('.*=.*',conf[i]):
        #new_conf[j]=conf[i]
        new_conf.append(conf[i])

def find_value(key):
    for i in range(len(new_conf)):
        p=re.compile(key)
        if None!=p.match(new_conf[i]):
            a=new_conf[i].split('=')
    return a[1].replace('\n','')

mode=find_value("mode")
eth0=find_value("cinter")
eth1=find_value("sinter")
cli_mac_s=find_value("cli_mac_s")
cli_mac_d=find_value("cli_mac_d")
sour_start_ip=find_value("sour_start_ip")
sour_ip_num=find_value("sour_ip_num")
sour_start_port=find_value("sour_start_port")
sour_port_num=find_value("sour_port_num")
ser_mac_s=find_value("ser_mac_s")
ser_mac_d=find_value("ser_mac_d")
dest_start_ip=find_value("dest_start_ip")
dest_ip_num=find_value("dest_ip_num")
dest_start_port=find_value("dest_start_port")
dest_port_num=find_value("dest_port_num")


def get_ip(ip,num):
    ip_new=[]
    ip_new[0]=ip
    for i in range(num-1)
        ip_start=ip.split('.')
        if ip_start[3]+i > 254 :
            ip4=(ip_start[3]+i)%254
            ip3=ip_n[2]+(ip_start[3]+num)/254
            if ip3 > 254 :
                tmp=ip3
                ip3=tmp%254
                ip2=ip_start[1]+tmp/254
                if ip2 > 254 :
                   tmp=ip2
                   ip2=tmp%254
                   ip1=ip_start[0]+tmp/254
        ip_new.append(ip1+"."+ip2+"."+ip3+"."+ip4)
    return ip_new


def get_file_path(pcap_path):
# pcap_path="pcaps"
    pcap_files=[]
    for parent,dirnames,filenames in os.walk(pcap_path):
        for filename in filenames: 
            if None!=re.search("pcap$",filename) :
                pcap_files.append(os.path.join(parent,filename))
    return pcap_files


def l2_send_pack(pcap_files):
    for repcap in pcap_files:
        p=re.compile("pcap$")
        cache=p.sub('cache',repcap)
        p=re.compile("pcap$")
        send_pcap=p.sub('send',repcap)
        cmd="tcpprep --auto=client --pcap="+repcap+" --cachefile="+cache
        tcpprep_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
        tcpprep_pipe.wait()
        if tcpprep_pipe.returncode==0 :
            cmd="tcpreplay --cachefile="+cache+" --intf1="+eth0+" --intf2="+eth1+" "+repcap
            print "start tcpreplay pcap:",repcap," waite..."
            tcpreplay_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
            tcpreplay_pipe.wait()
            if tcpreplay_pipe.returncode==0:
                print "packet:",repcap," replay complete\n\n"
            else:
                print "packet: ",repcap," replay failed"
                print "tcpreplay stdout: ",tcpreplay_pipe.stdout.read()
                print "tcpreplay stderr: ",tcpreplay_pipe.stderr.read()
        else:
            print "tcpprep error pcap:",repcap
            print "tcpprep error info:",tcpprep_pipe.stderr.read()




def l3_send_pack(pcap_files):
    for repcap in pcap_files:
        p=re.compile("pcap$")
        cache=p.sub('cache',repcap)
        p=re.compile("pcap$")
        send_pcap=p.sub('send',repcap)
        cmd="tcpprep --auto=client --pcap="+repcap+" --cachefile="+cache
        tcpprep_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
        tcpprep_pipe.wait()
        if tcpprep_pipe.returncode==0 :
            cmd="tcprewrite --enet-dmac="+ser_mac_d+","+cli_mac_d+" --enet-smac="+ser_mac_s+","+cli_mac_s+" --endpoints="+dest_start_ip+":"+sour_start_ip+" --skipbroadcast  --cachefile="+cache+" --infile="+repcap+" --outfile="+send_pcap
            tcprewrite_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
            tcprewrite_pipe.wait()
            if tcprewrite_pipe.returncode==0 :
                cmd="tcpreplay --cachefile="+cache+" --intf1="+eth0+" --intf2="+eth1+" "+send_pcap
                print "start tcpreplay pcap:",repcap," waite..."
                tcpreplay_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
                tcpreplay_pipe.wait()
                if tcpreplay_pipe.returncode==0:
                    print "packet:",repcap," replay complete\n\n"
                else:
                    print "packet: ",repcap," replay failed"
                    print "tcpreplay stdout: ",tcpreplay_pipe.stdout.read()
                    print "tcpreplay stderr: ",tcpreplay_pipe.stderr.read()
            else:
                print "tcprewrite error pcap:",repcap
                print "tcprewrite error info:",tcprewrite_pipe.stderr.read()
        else:
            print "tcpprep error pcap:",repcap
            print "tcpprep error info:",tcpprep_pipe.stderr.read()    


if mode == "2":
    print "path:",get_file_path(path)
    
    l2_send_pack(get_file_path(path))
elif mode == "3":
    print "path:",get_file_path(path)
    l3_send_pack(get_file_path(path))
else:
    print "replay.conf mode error"
    exit(255)

