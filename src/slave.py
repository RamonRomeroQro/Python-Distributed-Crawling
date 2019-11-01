#!/usr/bin/env python3

import socket, sys, pickle

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = int(sys.argv[1])        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            
            data_arr = pickle.loads(data)
            print ('Received', repr(data_arr))
            if not data:
                break
