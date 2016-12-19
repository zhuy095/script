#-*- coding: utf-8 -*-
#!/usr/bin/env python
# UDP Client - udpclient.py
# code by zhuyl
import socket, sys,time,threading,random,select,struct
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
    status=0
    sessionID=0
    runTime=time.time()
    smcRunTime=time.time()
    def __init__(self,ip):
        self.ip=ip
        self.sn='10076-0023I-2000T-E404P-'+str(10000+int(ip.split('.')[-1]))
        
    def _pack_header(self):
        sequence=2
        reserved=0
        version=2
        timestamp=time.time()
        header=struct.pack('!HbbHHif',version,self.command[0],self.command[1],sequence,reserved,self.sessionID,timestamp)
        return header
    
    def unpack_header(self,data):
        command=[0,0]
        if len(data) == 16 :
            ver,command[0],command[1],sequence,reserved,sessionID,timestamp=struct.unpack('!HbbHHif',data)
        else :
            ver,command[0],command[1],sequence,reserved,sessionID,timestamp,cloud_data=struct.unpack('!HbbHHif%ds'%(len(data)-16),data)
        if  command == [1,2] :  # 绑定应答报文
            self.sessionID=sessionID
            self.status = 1 #云端给绑定做应答，下次发送请求license
        elif command == [6,2] :  # update 
            self.license = cloud_data.decode('utf-8')
            self.status = 2  #license 更新后，只发送keepalive
        elif command == [6,3]: #收到云端发送的报活keepalive
            self.smcRunTime=time.time()  #收到smc的应答报文，更新smc在线时间。
            #pass
        return self.send_pack()
            
    def _send_bindcode(self):
        self.command=[1,1]
        data='{"sn": "'+self.sn+'", "bindCode": "aed995e7ce694c4287d9cd512e3d3229"}'
        return self._pack_header()+data.encode('ascii')
        
    def _send_licence_request(self):
        self.command=[6,1]
        self.core='{"core": "4"}'
        return self._pack_header()+self.core.encode('ascii')
    def _send_device_notice(self):  #agent keepalive
        self.command=[2,1]
        if self.status == 2 :
            dev_info='{"hostName": "'+self.ip+'", "hostIP": "'+self.ip+'", "version": "V1.1-R2.120161212", "uptime": "'+str(int(time.time()-self.runTime))+'", "cpuInfo": {"total": "100.00", "used": "0.00"}, "memInfo": {"total": "1096636116", "used": "455400072"}, "nrConns": "30", "nrUsers": "52", "cycle": "10", "license": '+self.license+'}'
        else :
            dev_info='{"hostName": "'+self.ip+'", "hostIP": "'+self.ip+'", "version": "V1.1-R2.120161212", "uptime": "'+str(int(time.time()-self.runTime))+'", "cpuInfo": {"total": "100.00", "used": "0.00"}, "memInfo": {"total": "1096636116", "used": "455400072"}, "nrConns": "30", "nrUsers": "52", "cycle": "10"}'
        return self._pack_header()+dev_info.encode('ascii')
        
    def send_pack(self):
        if int(time.time()-self.smcRunTime) > 300 :  #smc长时间不发送keepalive报文，则认为smc不在线，重新请求绑定。
            self.status=0
        if self.status == 0 : # 请求绑定
            return self._send_bindcode()
        elif self.status == 1:  # 请求license
            return self._send_licence_request(),self._send_device_notice()
        elif self.status == 2: # 只发送keepalive
            return self._send_device_notice()
        
def sendPackSocket(local_ip,port=2000):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((local_ip,port))
    s.setblocking(0)
    return s

def vfwScoket(ip_s):
    vfw_objs={}
    for i in range(len(ip_s)):
        sendSocket=sendPackSocket(ip_s[i])  #根据本地IP生成sock
        vfw=vfw_simulation(ip_s[i])  #根据IP生成vfw实例
        vfw_objs[sendSocket]=vfw   #把socket和vfw实例进行关联
    return vfw_objs
        
def run_main(vfw_objs):
    loops=0
    while True :
        rs,ws,es=select.select(vfw_objs.keys(),[],[],5) #,timeout=5
        if rs == []:  ## 如果超时，则发送保活报文，每5s发送一次。
            for sock in vfw_objs.keys():
                pack=vfw_objs[sock].send_pack()
                if type(pack) == tuple :  # status==2， 需要发送两个报文。
                    for i in range(len(pack)):
                        sock.sendto(pack[i],dest)
                else :
                    sock.sendto(pack,dest)
        else:  #vfw_objs.keys()被触发，有读操作(rs有返回值)。
            for sock in rs:   ##如果收到udp报文，则进行处理，并发送应答
                if sock in vfw_objs.keys():
                    message, address = sock.recvfrom(8192)
                    pack=vfw_objs[sock].unpack_header(message)
                    if type(pack) == tuple :
                        for i in range(len(pack)):
                            sock.sendto(pack[i],dest)
                    else :
                        sock.sendto(pack,dest)
        loops+=1
        print("loop %d"%loops)
        
if __name__ == '__main__' :
    #配置smc服务器IP
    dest_ip='192.168.1.221'
    port = 9070
    dest=(dest_ip,port)

    #配置vfw使用的本地
    local_ip='172.17.22.1'
    ip_num=100
    ip_list=ip_change(local_ip,ip_num)
    
    pdb.set_trace()
    vfw_objs=vfwScoket(ip_list)  #生成vfw和socket的对应关系
    run_main(vfw_objs)