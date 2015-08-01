#!/usr/bin/env python
import httplib,re,time,urllib,multiprocessing,signal,socket,subprocess

class HTTPConnection_with_ip_binding(httplib.HTTPConnection):
    def __init__(self, host, port=None, strict=None,timeout=socket._GLOBAL_DEFAULT_TIMEOUT, bindip=None):
        httplib.HTTPConnection.__init__(self,host,port,strict,timeout)
        self.bindip = bindip
    def connect(self):
        msg = "getaddrinfo returns an empty list"
        for res in socket.getaddrinfo(self.host, self.port, 0,socket.SOCK_STREAM):
            af,socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                if self.debuglevel > 0:
                    print "connect: (%s, %s)" % (self.host, self.port)
                if self.bindip is not None:
                    self.sock.bind((self.bindip,0))
                self.sock.connect(sa)
            except socket.error, msg:
                if self.debuglevel > 0:
                    print 'connect fail:', (self.host, self.port)
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error, msg

def get_ip(ip,num,ether,netmask):
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
    for i in range(len(ip_new_list)):
#        print("ether:%s;i :%s"%(ether,i))
        cmd='ifconfig '+ether+':'+str(i)+' '+ip_new_list[i]+netmask+' up'
        ip_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
        ip_pipe.wait()
        if ip_pipe.returncode!=0 :
            print("add local ip %s fail"%ip_new_list[i])
    return ip_new_list

def user_login(localip,key):
    http='192.168.0.238:8081'
    conn = HTTPConnection_with_ip_binding(host=http,bindip=localip)
    url1='/portal?'
    url2=(('wlanuserip',localip),('wlanacname','ZXJ'),('wlanusermac','00-0c-29-89-72-4f'))
    url3=urllib.urlencode(url2)
    url=url1+url3
    conn.request('GET', url) 
    httpers=conn.getresponse()
    headers=httpers.getheaders()
    cookie=headers[2][1]

    sendheader={"Accept-Encoding":"gzip, deflate","Accept":"*/*","Referer":"http://192.168.0.238:8081/static/portal/web/zh/freeload.html","Connection":"keep-Alive","Cookie":cookie,"Host":"192.168.0.238:8081"}
    conn.close()
#    print("cookie:%s"%cookie)
    sendheader['Content-type']="application/x-www-form-urlencoded; charset=UTF-8"
    sendheader['Accept-Language']="zh-cn"
    sendheader['Cache-Cotral']="no-cache"
    sendheader['Content-Length']="23"
    sendheader['User-Agent']="Mozilla/40 (compatible; MSIE 6.0; windows NT 5.1; SV1; LBBROWSER)"
    sendheader['x-requested-with']="XMLHttpRequest"
    auth=(('authCode',key),('authType','0'))
    sendbody=urllib.urlencode(auth)
    posturl='/portal/activeip'
    conn.request('POST',posturl,sendbody,sendheader)
    httpers=conn.getresponse()
    http=httpers.read()
    if None != re.search("true",http):
        print("%s login success"%localip)
    else:
        print("%s login fail"%locaoip)
#    print("%s login result:%s"%(localip,urllib.quote(http)))
#    print("%s login result:%s"%(localip,http))
    #print("%s login result:%s"%(localip,http['result']))
    conn.close()

def del_ip():
    for i in range(len(ipg)):
        cmd='ifconfig '+eth+':'+str(i)+'  down'
        ip_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
        ip_pipe.wait()
        if ip_pipe.returncode!=0 :
            print("del local ip %s fail"%ipg[i])
 
def handler(signum,frame):
    pool.terminate()
    del_ip()
    print "stop login!"

start_ip='192.168.222.1'
ip_num=100
key='2wa'
process_num=1
eth='eth1'
netmask='/16'

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGTERM, handler)

global pool,login_num
pool=multiprocessing.Pool(processes=process_num)
#login_num=0
ipg=get_ip(start_ip,ip_num,eth,netmask)
for i in range(len(ipg)):
   pool.apply_async(user_login,(ipg[i],key,))
pool.close()
pool.join()
#print("login success %i"%login_num)
del_ip()
