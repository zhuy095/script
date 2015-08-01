#!/usr/bin/env python

import socket,time,signal


def handler(signum,frame):
    s.close()
    print("exit")


addr=('172.16.0.20',2000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
data="aaaa"


signal.signal(signal.SIGINT, handler)
#    signal.signal(signal.SIGHUP, handler)
#    signal.signal(signal.SIGTERM, handler)

while 1:
    s.sendto(data,addr)
    print("send data:%s"%data)
    time.sleep(2)

