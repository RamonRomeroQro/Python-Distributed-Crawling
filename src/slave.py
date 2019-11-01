#!/usr/bin/env python3

import socket, sys

MASTER_HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
MASTER_PORT = 7000        # Port to listen on (non-privileged ports are > 1023)

SLAVE_HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
SLAVE_PORT = int(sys.argv[1] )       # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SLAVE_HOST, SLAVE_PORT))
    s.connect((MASTER_HOST, MASTER_PORT))
    #s.sendall(b'Hello, world')
    #data = s.recv(1024)

#print('Received', repr(data))


    