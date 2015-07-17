#!/usr/bin/env python
import httplib,re,time,urllib
#conn = httplib.HTTPConnection('www.baidu.com')
#conn.request('GET','/')
#httpers = conn.getresponse()
#headers=httpers.getheaders()
#url=headers[0][1]
#conn.close()

ip='192.168.222.13'
key='vj2'
http='192.168.0.238:8081'
conn = httplib.HTTPConnection(http)
url1='/portal?'
url2=(('wlanuserip',ip),('wlanacname','ZXJ'),('wlanusermac','00-0c-29-89-72-4f'))
url3=urllib.urlencode(url2)
url=url1+url3
conn.request('GET', url) 
httpers=conn.getresponse()
headers=httpers.getheaders()
cookie=headers[2][1]

sendheader={"Accept-Encoding":"gzip, deflate","Accept":"*/*","Referer":"http://192.168.0.238:8081/static/portal/web/zh/freeload.html","Connection":"keep-Alive","Cookie":cookie,"Host":"192.168.0.238:8081"}
conn.close()

print("cookie:%s"%cookie)

#conn = httplib.HTTPConnection(http)
#conn.request('GET', url,'',sendheader) 
#httpers=conn.getresponse()
#headers=httpers.getheaders()
#body=httpers.read()
#print("before_post body:%s"%body)

#if None!=re.search('introMessage',body):
#   time.sleep(10)

#conn.request('GET', url,'',sendheader) 
#httpers=conn.getresponse()
#body=httpers.read()
#print("before_post body:\n %s"%body)
#conn.close()

#post='post'
#if None!=re.search(post,body):
#    conn = httplib.HTTPConnection(http)
#    sendheader['Content-type']="application/x-www-form-urlencoded; charset=UTF-8"
#    sendheader['Accept-Language']="zh-cn"
#    sendheader['Cache-Cotral']="no-cache"
#    sendheader['Content-Length']="23"
#    sendheader['User-Agent']="Mozilla/40 (compatible; MSIE 6.0; windows NT 5.1; SV1; LBBROWSER)"
#    sendheader['x-requested-with']="XMLHttpRequest"
#    auth=(('authCode',key),('authType','0'))
#    sendbody=urllib.urlencode(auth)
    #posturl='/portal/login'
#    posturl='/portal/activeip'
#    conn.request('POST',posturl,sendbody,sendheader)
#    httpers=conn.getresponse()
#    http=httpers.read()
#    print("\n\n\n\nresult:%s"% http)
#    conn.close()

sendheader['Content-type']="application/x-www-form-urlencoded; charset=UTF-8"
sendheader['Accept-Language']="zh-cn"
sendheader['Cache-Cotral']="no-cache"
sendheader['Content-Length']="23"
sendheader['User-Agent']="Mozilla/40 (compatible; MSIE 6.0; windows NT 5.1; SV1; LBBROWSER)"
sendheader['x-requested-with']="XMLHttpRequest"
auth=(('authCode',key),('authType','0'))
sendbody=urllib.urlencode(auth)
#posturl='/portal/login'
posturl='/portal/activeip'
conn.request('POST',posturl,sendbody,sendheader)
httpers=conn.getresponse()
http=httpers.read()
print("\n\n\n\nresult:%s"% http)
conn.close()
