#!/usr/bin/env python3

import socket
from collections import deque

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 7000       # Port to listen on (non-privileged ports are > 1023)
LIMIT = 3

q=deque(['s','3'])

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
level=1
while True:
    while True:
        s.listen()
        aux=len(q)
        i=0
        while i<len(aux):
            conn, addr = s.accept()
            with conn:
                conn.sendall(q.pop().encode())
            i+=1
            
    #retrive
    if not q or level==LIMIT:
        break
    level+=1
