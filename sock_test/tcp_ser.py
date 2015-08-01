#!/usr/bin/env python

import socket,signal

def handler(signum,frame):
    s.close()
    print("exit")


host=''
port=3000

s=socket.socket( socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
s.bind((host, port))
s.listen(1)

signal.signal(signal.SIGINT, handler)
#    signal.signal(signal.SIGHUP, handler)
#    signal.signal(signal.SIGTERM, handler)


while 1:
    csock,caddr=s.accept()
#    print("get connected by %s"%caddr)
    while 1:
        data=csock.recv(8192)
        if len(data)==0:
            break
        print("get data: %s"% data)
        csock.sendall(data)

