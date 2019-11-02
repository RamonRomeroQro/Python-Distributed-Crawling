import struct
import json
import socket
import pickle
with open('./settings.json') as f:
    settings = json.load(f)

NUM_SLAVES = len(settings['slaves'])
MASTER_HOST = settings['master']['ip']  # The server's hostname or IP address
MASTER_PORT = settings['master']['port']        # The port used by the server

def main():

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((MASTER_HOST, MASTER_PORT))
    my_socket.listen(NUM_SLAVES)

    print("Server is running on " + str(MASTER_PORT))

    list_connections = []

    for i in range(NUM_SLAVES):
        c, addr = my_socket.accept()
        list_connections.append((c, addr))

    retrived_list = ['a'*x for x in range(1, 10)]
    send_list = [[] for x in range(NUM_SLAVES)]

    for i, v in enumerate(retrived_list):
        send_list[i % NUM_SLAVES].append(v)

    for j, pair in enumerate(list_connections):
        packet = pickle.dumps(send_list[j])
        length = struct.pack('!I', len(packet))
        packet = length + packet
        pair[0].sendall(packet)

    my_socket.close()
    return 0

if __name__ == "__main__":
    main()
