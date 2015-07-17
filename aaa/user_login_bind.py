#!/usr/bin/env python
import httplib,re,time,urllib,multiprocessing,signal,socket

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
    print("%s login result:%s"%(localip,http))
    conn.close()

def handler(signum,frame):
    pool.terminate()
    print "closed tcprelay!"

localip='192.168.222.15'
key='vj2'
process_num=100

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGTERM, handler)

pool=multiprocessing.Pool(processes=process_num)

ipg=get_ip(ip,100)

