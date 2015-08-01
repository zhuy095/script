#!/usr/bin/env python
import struct,socket,re,time,threading

def ip_to_struct(ip):
    ipn=ip.split('.')
    ipa=[]
    for i in range(len(ipn)):
        ipa.append(struct.pack('B',int(ipn[i])))
    return ''.join(ipa)

def udp_tlv1(authip,acip,key,sNo):
    ver=struct.pack('B',1)
    tpye=struct.pack('B',3)
    auth_type=struct.pack('B',1)
    rsv=struct.pack('B',0)
    SerialNo=struct.pack('H',int(sNo))
    ReqID=struct.pack('H',0)
    UserIP=ip_to_struct(authip)
    UserPort=struct.pack('H',0)
    ErrCode=struct.pack('B',0)
    AttrNum=struct.pack('B',4)
    tlv_header=ver+tpye+auth_type+rsv+SerialNo+ReqID+UserIP+UserPort+ErrCode+AttrNum

    #attr username
    attrType=struct.pack('B',1)
    UserName=key+"0001@syxa"
    l=len(UserName)+2
    attrLen=struct.pack('B',l)
    attrUser=attrType+attrLen+UserName

    #attr passwd
    attrType=struct.pack('B',2)
    Passwd=key+"0001"
    l=len(Passwd)+2
    attrLen=struct.pack('B',l)
    attrPasswd=attrType+attrLen+Passwd

    #attr last
    last=[]
    last.append(struct.pack('B',10))
    last.append(struct.pack('B',6))
    last.append(ip_to_struct(acip))
    last.append(struct.pack('B',128))
    last.append(struct.pack('B',2))
    attrLast=''.join(last)

    return tlv_header+attrUser+attrPasswd+attrLast

def udp_tlv3(UserIP,acip,sNo):
#def udp_tlv2(authip,acip,sNo):
    ver=struct.pack('B',1)
    tpye=struct.pack('B',7)
    auth_type=struct.pack('B',0)
    rsv=struct.pack('B',0)
#    SerialNo=struct.pack('H',int(sNo))
    ReqID=struct.pack('H',0)
#    UserIP=ip_to_struct(authip)
    UserPort=struct.pack('H',0)
    ErrCode=struct.pack('B',0)
    AttrNum=struct.pack('B',2)
    tlv_header=ver+tpye+auth_type+rsv+sNo+ReqID+UserIP+UserPort+ErrCode+AttrNum

    #attr last
    last=[]
    last.append(struct.pack('B',10))
    last.append(struct.pack('B',6))
    last.append(acip)
    #last.append(ip_to_struct(acip))
    last.append(struct.pack('B',128))
    last.append(struct.pack('B',2))
    attrLast=''.join(last)

    return tlv_header+attrLast

def get_last(pcap):
    UserIP=pcap[8:12]
    acip=pcap[18:22]
    sNo=pcap[4:6]
    udp_data=udp_tlv3(UserIP,acip,sNo)
#    s.send(udp_data)
    return udp_data

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

def get_first(AuthIp,AcIp,key,sNo,ip_nums):
    sNo=1001
    ipg=get_ip(AuthIp,ip_nums)
    pcaps=[]
    for i in range(ip_nums):
        sNo+=2
        pcaps.append(udp_tlv1(ipg[i],AcIp,key,sNo))
    return pcaps


def send_first(pcaps,s,remotehost,speed,isfor):
    lo=count=0
    if int(isfor) == int(1):
        while 1:
            for i in range(len(pcaps)):
                s.sendto(first_pcaps[i],remotehost)
                lo+=1
                if int(lo) == int(speed)  :
                    count+=lo
                    lo=0
                    print("auth:%i"%count)
                    time.sleep(1)
    else:
        for i in range(len(pcaps)):
            s.sendto(first_pcaps[i],remotehost)
            lo+=1
            if int(lo) == int(speed)  :
                count+=lo
                lo=0
                print("auth:%i"%count)
                time.sleep(1)

def rev_pcap(s):
    while 1:
        message, address = s.recvfrom(8192)
        print "Got data :", message
    #    pcap=udp_tlv1(AuthIp,AcIp,key,sNo)
    #    print("pcap:",pcap)
        send_pcap=get_last(message)
        s.sendto(send_pcap,address)


#host = ''
#port = 50100
AcIp='192.168.1.19'
AuthIp='192.168.80.1'
ip_nums=30000
key='3dk'
sNo='200'
isfor=1
speed=400
localhost=('192.168.2.104',50100)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.bind((host, port))
s.bind(localhost)
s.setblocking(0)

remotehost=('192.168.1.19',2000)
first_pcaps=get_first(AuthIp,AcIp,key,sNo,ip_nums)
#print first_pcaps
threads=[]
send_f=threading.Thread(target=send_first,args=(first_pcaps,s,remotehost,speed,isfor))
threads.append(send_f)
send_f=threading.Thread(target=rev_pcap,args=(s,))
threads.append(send_f)
print "set threads"
for f in range(len(threads)):
    threads[f].start()
    threads[f].join()

