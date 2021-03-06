﻿#-*- coding: utf-8 -*-
#!/usr/bin/env python
# UDP Client - udpclient.py
# code by zhuyl
#from gevent import select
from gevent import monkey; monkey.patch_all()
import socket
import gevent
import sys
import time
import random
import struct
import json
import os
import pdb

def ip_change(startip='',count=None):
    ip=[startip]
    ip_old=startip.split('.')
    for i in range(count-1):
        ip_old[3]=int(ip_old[3])+1
        if int(ip_old[3]) == 255 :
            ip_old[3]=1
            ip_old[2]=int(ip_old[2])+1
            if int(ip_old[2]) == 255 :
                ip_old[2] = 1
                ip_old[1] = int(ip_old[1])+1
                if int(ip_old[1])==255:
                    ip_old[1] = 1
                    ip_old[0] = int(ip_old[0])+1
        for a in range(len(ip_old)):
            ip_old[a]=str(ip_old[a])
        ip.append('.'.join(ip_old))
    return ip

class vfw_simulation():  #vfw 实例

    def __init__(self,ip,core):
        self.ip=ip
        self.sn='00020003-0004-0005-0006-00070008'+str('{:p>4}'.format(ip.split('.')[-1]))
        self.status=0
        self.sessionID=0
        self.sequence=1
        self.runTime=time.time()
        self.smcRunTime=time.time()
        self.license='no license'
        self.core=core
        
    def _pack_header(self):
        self.sequence=(self.sequence+1) if self.sequence <= 65535 else 1
        #self.sequence+=1
        #if self.sequence > 65535:
        #    self.sequence=0
        reserved=0
        version=2
        timestamp=time.time()
        header=struct.pack('!HbbHHif',version,self.command[0],self.command[1],self.sequence,reserved,self.sessionID,timestamp)
        return header
    
    def unpack_header(self,data):
        command=[0,0]
        if len(data) == 16 :
            ver,command[0],command[1],sequence,reserved,sessionID,timestamp=struct.unpack('!HbbHHif',data)
        else :
            ver,command[0],command[1],sequence,reserved,sessionID,timestamp,cloud_data=struct.unpack('!HbbHHif%ds'%(len(data)-16),data)
        if  command == [1,2] :  # 绑定应答报文
            self.sessionID=sessionID
            self.status = 2 #云端给绑定做应答，下次发送请求license
        #elif command == [6,2] :  # update 
        #    self.license = json.loads(cloud_data.decode('utf-8'))
        #    self.status = 2  #license 更新后，只发送keepalive
        #elif command == [6,3]: #收到云端发送的报活keepalive
        #    self.smcRunTime=time.time()  #收到smc的应答报文，更新smc在线时间。
            #pass
        return self.send_pack()
            
    def _send_bindcode(self):
        self.command=[1,1]
        data={"sn":self.sn, "bindCode":"aed995e7ce694c4287d9cd512e3d3229"}
        return self._pack_header()+json.dumps(data).encode('ascii')
        
    def _send_licence_request(self):
        self.command=[6,1]
        coretxt={"core":self.core}
        return self._pack_header()+json.dumps(coretxt).encode('ascii')
    def _send_device_notice(self):  #agent keepalive
        self.command=[2,1]
        dev_info={"hostName":self.ip, "hostIP": self.ip, "version": "V1.1-R2.120161212", "uptime":str(int(time.time()-self.runTime)), "cpuInfo": {"total": "100.00", "used": "0.00"}, "memInfo": {"total": "1096636116", "used": "455400072"}, "nrConns": "30", "nrUsers": "52", "cycle": "10"}
        if self.status == 2 :
            dev_info["license"]=self.license
        return self._pack_header()+json.dumps(dev_info).encode('ascii')
        
    def send_pack(self):
        if int(time.time()-self.smcRunTime) > 1200 :  #smc长时间不发送keepalive报文，则认为smc不在线，重新请求绑定。
            self.__init__(self.ip)
        if self.status == 0 : # 请求绑定
            return self._send_bindcode()
        elif self.status == 1:  # 请求license
            return self._send_licence_request(),self._send_device_notice()
        elif self.status == 2: # 只发送keepalive
            return self._send_device_notice()
        
def headles(local_ip,dest_ip,core):
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.bind((local_ip,2000))
    #sock.setblocking(0)
    #sock.connect(dest_ip)
    vfw=vfw_simulation(local_ip,core)
    while True:
        data = None
        with gevent.Timeout(5,False):
            data,address=sock.recvfrom(8192)
        if data is None :
            pack=vfw.send_pack()
            sock.sendto(pack,dest_ip)
            print("from %s  connect to %s "%(str(sock.getsockname()),str(dest_ip)))
        else :
            pack=vfw.unpack_header(data)
            if type(pack) == tuple :
                for i in range(len(pack)):
                    sock.sendto(pack[i],dest_ip)
            print("from %s  connect to %s "%(str(sock.getsockname()),str(address)))
                    
def run_main(ip_list,dest_ip,core):
    even=[]  #事件驱动，存放事件
    #gevent.joinall([
    #gevent.spawn(headles,ip_list[0],dest_ip,core),
    #gevent.spawn(headles,ip_list[1],dest_ip,core)
    #])
    for ip in ip_list:
        even.append(gevent.spawn(headles,ip,dest_ip,core))
    gevent.joinall(even)

if __name__ == '__main__' :
    #配置smc服务器IP
    dest_ip='172.17.10.95'
    #dest_ip='172.18.10.97'
    port = 9070
    dest=(dest_ip,port)

    #配置vfw使用的本地
    local_ip='172.17.25.1'
    core=4
    ip_num=300
    ip_list=ip_change(local_ip,ip_num)
    pdb.set_trace()
    run_main(ip_list,dest,core)