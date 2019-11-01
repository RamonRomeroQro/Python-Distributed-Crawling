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

retrived_list = ['a'*x for x in range(1, 10)]
send_list = [[] for x in range(NUM_SLAVES)]

for i, v in enumerate(retrived_list):
    send_list[i % NUM_SLAVES].append(v)


for j, pair in enumerate(SLAVE_SOCKETS):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(pair)
        packet = pickle.dumps(send_list[j])
        length = struct.pack('!I', len(packet))
        packet = length + packet
        s.sendall(packet)
