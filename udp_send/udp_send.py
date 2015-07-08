#!/usr/bin/env python
# UDP Client - udpclient.py
# code by www.cppblog.com/jerryma
import socket, sys,time,threading

dest_ip='192.168.2.103'
port = 1000
data_length=512

count=[0,0]
def get_send_data(length):
    data=''
    for i in  range(int(length-42)) :
        data+="a"
    return data

def timer_start():
    t = threading.Timer(1, print_send_num)
    t.start()

def print_send_num():
    print "send udp pps:",count[0]-count[1]
    print "count[0]=",count[0],"count[1]=",count[1]
    count[1]=count[0]
    timer_start()

data=get_send_data(data_length)


host = (dest_ip,port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


timer_start()
while 1:
    s.sendto(data,host)
    count[0]+=1
#    if count[0] > 1000000:
#        break
 
