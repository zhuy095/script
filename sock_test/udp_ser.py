#!/usr/bin/env python
import socket,signal

def handler(signum,frame):
    s.close()
    print("exit")

host = ''
port = 2000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

signal.signal(signal.SIGINT, handler)
#    signal.signal(signal.SIGHUP, handler)
#    signal.signal(signal.SIGTERM, handler)


while 1:
    try:
        message, address = s.recvfrom(8192)
        print "Got data :", message
        s.sendto(message, address)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
