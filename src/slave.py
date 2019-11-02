import struct
import json
import socket
import pickle
with open('./settings.json') as f:
    settings = json.load(f)

NUM_SLAVES = len(settings['slaves'])
SLAVE_SOCKETS = [(s['ip'], s['port']) for s in settings['slaves']]
MASTER_HOST = settings['master']['ip']  # The server's hostname or IP address
MASTER_PORT = settings['master']['port']        # The port used by the server


def aux():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.bind((HOST, PORT))
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

def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((MASTER_HOST, MASTER_PORT))
        s.sendall(b'ready')
        sn = s.recv(1024)
        print('crawling',repr(sn))
        s.sendall(b'finished')


def main():
    connect()
if __name__ == "__main__":
    main()