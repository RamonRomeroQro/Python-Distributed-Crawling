import struct
import json
import socket
import pickle
import sys
from DataManagement import DataManager
from pymongo import MongoClient

f = open('./../settings.json')
settings = json.load(f)
f.close()

NUM_SLAVES = len(settings['slaves'])
MASTER_HOST = settings['master']['ip']  # The server's hostname or IP address
MASTER_PORT = settings['master']['port']        # The port used by the server
MASTER_DB = settings['master']['db']        # The port used by the server
KWORDS = set(settings['kwords'])
SEEDS = set(settings['seeds'])


def main():
    # set socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((MASTER_HOST, MASTER_PORT))
    my_socket.listen(NUM_SLAVES)

    print("Server is running on " + str(MASTER_PORT))
    # wait for requests
    list_connections = []
    i = 0
    while i < NUM_SLAVES:
        c, addr = my_socket.accept()
        list_connections.append((c, addr))
        i += 1

    # data retriever

    db = DataManager(MASTER_HOST, MASTER_DB, NUM_SLAVES)
    try:
        db.add_seeds(SEEDS)
    except Exception as e:
        print("seeds duplicadas, continuando amplitud")

    # while crawlables
    client = db.client
    database = client['dataset']
    links_collection = database['links']


    while links_collection.count_documents({ 'crawled': False }, limit = 1):
        print('crawl')

        send_list = db.get_crawlable()

        for j, pair in enumerate(list_connections):
            pair[0].sendall(pickle.dumps(send_list[j]))
            # packet = pickle.dumps(send_list[j])
            # length = struct.pack('!I', len(packet))
            # packet = length + packet
            # pair[0].sendall(packet)

        #my_socket.close()
        flat = []
        for l in send_list:
            for e in l:
                flat.append(e['url'])

        # traverse level
        while True:
            c = 0
            for x in flat:
                myquery = {"url": x}
                r = links_collection.find(myquery)
                for x in r:
                    if x['crawled'] == True:
                        c += 1
            if c == len(flat):
                break
        print("finshed level")

        my_socket.close()
        client.close()
    return 0


if __name__ == "__main__":
    main()
