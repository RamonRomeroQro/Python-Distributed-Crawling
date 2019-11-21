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

    
        for i, d_element in enumerate(send_list):
            packet = pickle.dumps(d_element)
            length = struct.pack('!I', len(packet))
            packet = length + packet
            list_connections[i%len(list_connections)][0].sendall(packet)

        #my_socket.close()
        

        # traverse level
        while True:
            c = 0
            for d_e in send_list:

                myquery = {"url": d_e['url']}
                r = links_collection.find(myquery)
                for x in r:
                    if x['crawled'] == True:
                        c += 1
            if c == len(send_list):
                break
        print("finshed level")

        my_socket.close()
        client.close()
    return 0


if __name__ == "__main__":
    main()
