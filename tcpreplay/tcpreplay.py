#!/usr/bin/python

import os,commands,thread
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
cinter=find_value("cinter")
sinter=find_value("sinter")
cli_mac_d=find_value("cli_mac_d")
sour_start_ip=find_value("sour_start_ip")
sour_ip_num=find_value("sour_ip_num")
#sour_start_port=find_value("sour_start_port")
#sour_port_num=find_value("sour_port_num")
ser_mac_d=find_value("ser_mac_d")
dest_start_ip=find_value("dest_start_ip")
dest_ip_num=find_value("dest_ip_num")
#dest_start_port=find_value("dest_start_port")
#dest_port_num=find_value("dest_port_num")


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


def get_file_path(pcap_path):
# pcap_path="pcaps"
    pcap_files=[]
    for parent,dirnames,filenames in os.walk(pcap_path):
        for filename in filenames: 
            if None!=re.search("pcap$",filename) :
                pcap_files.append(os.path.join(parent,filename))
    return pcap_files

def ip_to_mac(ip):
    mac_old=ip.split('.')
    for i in range(len(mac_old)):
        mac_old[i]=hex(int(mac_old[i])).replace('0x','')
        if len(mac_old[i] ) == 1:
            mac_old[i]=str(0)+mac_old[i]
    mac_new="02:02:"+str(mac_old[0])+":"+str(mac_old[1])+":"+str(mac_old[2])+":"+str(mac_old[3])
    return mac_new


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
            cmd="tcpreplay --cachefile="+cache+" --intf1="+cinter+" --intf2="+sinter+" "+repcap
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






def l3_send_pack(repcap,ser_mac_d,cli_mac_d,ser_mac_s,cli_mac_s,dest_start_ip,sour_start_ip):
    p=re.compile("pcap$")
    cache=p.sub('cache',repcap)
    p=re.compile("pcap$")
    tmp=dest_start_ip+"_"+sour_start_ip
#    send_pcap=p.sub('send',repcap)
    send_pcap=p.sub(tmp,repcap)
    cmd="tcpprep --auto=client --pcap="+repcap+" --cachefile="+cache
    tcpprep_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
    tcpprep_pipe.wait()
    if tcpprep_pipe.returncode==0 :
        cmd="tcprewrite --enet-dmac="+cli_mac_d+","+ser_mac_d+" --enet-smac="+cli_mac_s+","+ser_mac_s+" --endpoints="+sour_start_ip+":"+dest_start_ip+" --skipbroadcast  --cachefile="+cache+" --infile="+repcap+" --outfile="+send_pcap
        # cmd="tcprewrite --enet-dmac="+ser_mac_d+","+cli_mac_d+" --enet-smac="+ser_mac_s+","+cli_mac_s+" --endpoints="+dest_start_ip+":"+sour_start_ip+" --skipbroadcast  --cachefile="+cache+" --infile="+repcap+" --outfile="+send_pcap
        tcprewrite_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
        tcprewrite_pipe.wait()
        if tcprewrite_pipe.returncode==0 :
            cmd="tcpreplay --cachefile="+cache+" --intf1="+cinter+" --intf2="+sinter+" "+send_pcap
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

def l3_send_packs(pcap_files):
    s_ip=get_ip(sour_start_ip,sour_ip_num)
    print "sour_ip",s_ip
    d_ip=get_ip(dest_start_ip,dest_ip_num)
    print "dest_ip",d_ip
    print "pcap_files:",pcap_files
    for pcap in pcap_files:
        for snum in range(int(sour_ip_num)):
            smac_c=ip_to_mac(s_ip[snum])
            for dnum in range(int(dest_ip_num)):
               smac_s=ip_to_mac(d_ip[dnum])
               print "pcap:",pcap
               print "ser_mac_d",ser_mac_d
               print "cli_mac_d",cli_mac_d
               print "smac_s",smac_s
               print "smac_c",smac_c
               print "d_ip[",dnum,"] =",d_ip[dnum]
               print "s_ip[",snum,"] =",s_ip[snum]
              # thread.start_new_thread(l3_send_pack,(pcap,ser_mac_d,cli_mac_d,smac_s, smac_c,d_ip[dnum],s_ip[snum]))
               
               l3_send_pack(pcap,ser_mac_d,cli_mac_d,smac_s, smac_c,d_ip[dnum],s_ip[snum])



if mode == "2":
#    print "path:",get_file_path(path)
    print "a"
#    l2_send_pack(get_file_path(path))
elif mode == "3":
#    print "path:",get_file_path(path)
    l3_send_packs(get_file_path(path))
#    a=get_ip("192.168.1.10",5000)

 #   print "a:",a
else:
    print "replay.conf mode error"
    exit(255)

