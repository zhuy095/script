#!/usr/bin/python
import socket,time,signal

def handler(signum,frame):
    print("exit")
    s.close()



HOST='172.16.0.20'
PORT=3000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      
s.connect((HOST,PORT))       
print("Ctrl+c to stop")

signal.signal(signal.SIGINT, handler)
#    signal.signal(signal.SIGHUP, handler)
#    signal.signal(signal.SIGTERM, handler)

while 1:
    data="aaaa"
    s.sendall(data)  
    data=s.recv(1024)  
    print data         
    time.sleep(2)


