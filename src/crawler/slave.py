import struct
import json
import socket
import pickle
import sys
from Crawler import Crawler
with open('./../settings.json') as f:
    settings = json.load(f)

ID = sys.argv[1]
NUM_SLAVES = len(settings['slaves'])
SLAVE_SOCKETS = [(s['ip'], s['port']) for s in settings['slaves']]
MASTER_HOST = settings['master']['ip']  # The server's hostname or IP address
MASTER_PORT = settings['master']['port']        # The port used by the server
KWORDS = set(settings['kwords'])
SEEDS = set(settings['seeds'])


def connect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((MASTER_HOST, MASTER_PORT))
        #Reciving Hear
        d_url={}
        while True:
            while True:
                buf = b''
                while len(buf) < 4:
                    buf += s.recv(4 - len(buf))
                length = struct.unpack('!I', buf)[0]
                data = s.recv(length)
                d_url = pickle.loads(data)
                break

            print(d_url)


            #print('crawling', i)
            crawler_instance = Crawler(d_url, KWORDS, ID)
            crawler_instance.inspect_images()
            crawler_instance.inspect_urls()
            crawler_instance.update_current()
            crawler_instance.client.close()


def main():
    connect()


if __name__ == "__main__":
    main()
