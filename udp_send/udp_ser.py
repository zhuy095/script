#!/usr/bin/env python
# UDP Echo Server -  udpserver.py
# code by www.cppblog.com/jerryma
import socket, traceback

host = ''
port = 1000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

while 1:
    try:
        message = s.recv(8192)
#        message, address = s.recvfrom(8192)
#        print "Got data , length:", len(message)
#        s.sendto(message, address)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
