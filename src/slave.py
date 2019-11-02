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


def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((MASTER_HOST, MASTER_PORT))
        while True:
            buf = b''
            while len(buf) < 4:
                buf += s.recv(4 - len(buf))
            length = struct.unpack('!I', buf)[0]
            data = s.recv(length)
            data_arr = pickle.loads(data)
            break

        for i in data_arr:
            print('crawling', i)


def main():
    connect()


if __name__ == "__main__":
    main()
