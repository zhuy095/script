#!/usr/bin/python
import socket,time
HOST='172.16.0.20'
PORT=3000


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      
s.connect((HOST,PORT))       
while 1:
    data="aaaa"
    s.sendall(data)  
    data=s.recv(1024)  
    print data         
    time.sleep(2)
s.close() 

