#-*- coding: utf-8 -*-
#!/usr/bin/env python
# smc server
# code by zhuyl
import socket, sys,time,threading,random,select,struct,json
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

    def __init__(self,ip):
        self.ip=ip
        self.status=0
        self.sequence=0
        self.sessionID=random.randint(1,2147483648)
        self.runTime=time.time()
        self.license_status=1
    
    def _pack_header(self):
        reserved=0
        version=2
        timestamp=time.time()
        self.sequence+=1
        header=struct.pack('!HbbHHif',version,self.command[0],self.command[1],self.sequence,reserved,self.sessionID,timestamp)
        return header
        
    def unpack_header(self,data):
        command=[0,0]
        if len(data) == 16 :
            ver,command[0],command[1],sequence,reserved,sessionID,timestamp=struct.unpack('!HbbHHif',data)
        else :
            ver,command[0],command[1],sequence,reserved,sessionID,timestamp,cloud_data=struct.unpack('!HbbHHif%ds'%(len(data)-16),data)
        self.devRunTime=time.time()
        if  command == [1,1] :  # 请求绑定
            self.status = 1 # 进入应答绑定状态
        elif command == [6,1] :  # 请求license
            self.status = 2  # 进入license 应答状态
        elif command == [2,1]: # dev报活报文
            if not hasattr(self,'keepalivetime'):
                self.keepalivetime=time.time()
            self.status = 3
        return self.send_pack()
            
    def _access_bindcode(self):
        self.command=[1,2]
        return self._pack_header()
        
    def _send_licence(self): # smc send license
        self.command=[6,2]
        self.license={"ngfw":{"status":"on","point":"0"},"app":{"status":"on","point":"0"},"ips":{"status":"on","point":"0"},"av":{"status":"on","point":"0"},"url":{"status":"on","point":"0"},"ipsec":{"status":"on","point":"0"},"app_s":{"status":"on","point":"0"},"ips_s":{"status":"on","point":"0"},"av_s":{"status":"on","point":"0"},"url_s":{"status":"on","point":"0"},"ipsec_c":{"status":"on","point":"20"}}
        if random.randint(1,100)%2 == 0 :
            self.license['app']['status']='off'
            self.license['ips']['status']='off'
            self.license['ips_s']['status']='off'
        return self._pack_header()+json.dumps(self.license).encode('ascii')
        
    def _send_keepalive(self):  #smc keepalive
        self.command=[6,3]
        return self._pack_header() 
        
    def send_pack(self):
        pack=None
        if not hasattr(self,"devRunTime") or int(time.time()-self.devRunTime) > 300 :  #dev长时间不发送keepalive报文，则认为dev不在线，重新请求绑定。
                self.__init__(self.ip)
        if self.status == 1 : # 请求绑定
            pack=self._access_bindcode()
        elif self.status == 2:  # 请求license
            self.status == 3
            self.keepalivetime=time.time()
            pack=self._send_licence()
        elif self.status == 3: # 发送keeplive
            if time.time()-self.keepalivetime > 20 :
                self.keepalivetime=time.time()
                pack=self._send_keepalive()
                self.license_status*=-1
                if self.license_status == -1 :
                    pack=[pack,self._send_licence()]
        return pack
        
def sendPackSocket(local_ip,port=9070):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((local_ip,port))
    s.setblocking(0)
    return s
        
def run_main(socket):
    loops=0
    devs={}
    while True :
        rs,ws,es=select.select([socket],[],[],10) #,timeout=5
        if rs == []:  ## 如果超时，则发送保活报文，每5s发送一次。
            for address in devs.keys():
                pack=devs[address].send_pack()
                try:
                    if type(pack) == bytes :
                        sock.sendto(pack,address)
                    elif type(pack) == list:
                        for p in pack:
                            sock.sendto(p,address)
                except BlockingIOError:
                    if address in devs.keys():
                        del devs[address]
        else:  #vfw_objs.keys()被触发，有读操作(rs有返回值)。
            for sock in rs :
                try:
                    message,address=sock.recvfrom(8192)
                    if address not in devs.keys() :
                        devs[address]=vfw_simulation(address)
                    pack=devs[address].unpack_header(message)
                    if type(pack) == bytes :
                        sock.sendto(pack,address)
                    elif type(pack) == list:
                        for p in pack:
                            sock.sendto(p,address)
                except ConnectionResetError :
                    if address in devs.keys():
                        del devs[address]
        loops+=1
        print("loop %d"%loops)

def show_license(devs):
    vfws=tuple(devs.values())
    for i in range(len(vfws)):
        print("IP: {0}".format(vfws[i].ip))
        if hasattr(vfws[i],'license'):
            print("License: {0}".format(vfws[i].license))

if __name__ == '__main__' :
    local_ip='172.17.20.25'
    pdb.set_trace()
    run_main(sendPackSocket(local_ip,9070))