import socket
import sys
import pickle
import struct

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# Port to listen on (non-privileged ports are > 1023)
PORT = int(sys.argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            buf = b''
            while len(buf) < 4:
                buf += conn.recv(4 - len(buf))
            length = struct.unpack('!I', buf)[0]
            data = conn.recv(length)
            data_arr = pickle.loads(data)
            print('Received', repr(data_arr))
            break
