#!/usr/bin/env python


import socket,time
addr=('172.16.0.20',2000)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

data="aaaa"

while 1:
    s.sendto(data,addr)
    print("send data:%s"%data)
    time.sleep(2)

s.close
