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

from multiprocessing import Process
from collections import deque

q=deque(['a','3','3'])
clients = []

def clientHandler(c, addr):
    global clients
    print(addr, "is Connected")
    
    while True:
        data = c.recv(1024) # ready
        print(repr(data))
        if not data: 
            break 
        if data.decode() =="ready":
            nd=q.popleft()
            c.sendall(nd.encode())
        elif data.decode() =="finished":
            break

   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((MASTER_HOST, MASTER_PORT))
s.listen(NUM_SLAVES)

print("Server is running on "+ str(MASTER_PORT))

#Thread(target=clientHandler).start()
#Thread(target=clientHandler).start()
#Thread(target=clientHandler).start()
trds = []

ox=[]

for i in range(NUM_SLAVES): 
    c, addr = s.accept() 
    clients.append(addr)
    ox.append((c,addr))

for i in ox:
    t = Process(target=clientHandler, args = (i[0], i[1]))
    trds.append(t)
    t.start()

for t in trds:
    t.join()

s.close()