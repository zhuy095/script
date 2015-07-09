#!/usr/bin/env python
# UDP Client - udpclient.py
# code by www.cppblog.com/jerryma
import socket, sys,time,threading

dest_ip='127.0.0.1'
port = 1000
data_length=64

count1=[long(0),long(0)]
count2=[long(0),long(0)]
def get_send_data(length):
    data=''
    for i in  range(int(length-42)) :
        data+="a"
    return data

def timer_start():
    t = threading.Timer(1, print_send_num)
    t.start()

def print_send_num(*count):
    pps=int(count1[0])-int(count1[1])+int(count2[0]-int(count2[1]))
#    print "count1[0]=",count1[0]
#    print "count2[0]=",count2[0]
#    print "count1[1]=",count1[1]
#    print "count2[1]=",count2[1]
    count1[1]=count1[0]
    count2[1]=count2[0]
    print "send udp pps:",pps
    #    print "count[0]=",count[0],"count[1]=",count[1]
#    count[1]=count[0]
    timer_start()

data=get_send_data(data_length)

def send_pack(port,num):
    host = (dest_ip,port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    timer_start()
    while 1:
        s.sendto(data,host)
        num[0]+=1
#        print "send pack:",num
#        if num[0] > 1000000:
#            break

threads=[]
t1=threading.Thread(target=send_pack,args=(int(1000),count1,))
threads.append(t1)
t2=threading.Thread(target=send_pack,args=(int(1000),count2,))
threads.append(t2)

if __name__=='__main__':
    timer_start()
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print " all is over"

 
