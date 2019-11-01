#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 7000       # Port to listen on (non-privileged ports are > 1023)

urls=['goo.txt']



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    conections=[]
    while True:
        s.listen()
        conn, addr = s.accept() 
        conections.append( addr)
        if len(conections)==2:
            break
    print(conections)

    # with conn:
    #     print('Connected by', addr)
    #     while True:
    #         data = conn.recv(1024)
    #         if not data:
    #             break
    #         conn.sendall(data)