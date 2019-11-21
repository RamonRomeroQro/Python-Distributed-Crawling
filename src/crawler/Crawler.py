from bs4 import BeautifulSoup
from collections import deque
import requests
from pymongo import MongoClient
import os

import json
# import re
f = open('./../settings.json')
settings = json.load(f)
f.close()

NUM_SLAVES = len(settings['slaves'])
MASTER_HOST = settings['master']['ip']  # The server's hostname or IP address
MASTER_PORT = settings['master']['port']        # The port used by the server
MASTER_DB = settings['master']['db']        # The port used by the server
KWORDS = set(settings['kwords'])
SEEDS = set(settings['seeds'])


class Crawler:
    def __init__(self, dict_db, kwords_v, id_v):
        self.dict_v = dict_db
        self.url = self.dict_v['url']
        self.id = id_v
        self.base = self.url[:self.g_base()]

        self.kwords = kwords_v
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, features="html.parser")

    def beautiful(self):
        return self.soup.prettify()

    def g_base(self):
        c=0
        for i,e in enumerate(self.url):
            if e=='/':
                c+=1
            if c==3:
                return i
        return len(self.url)

    def bfs(self):
        queue = deque([self.soup])  # queue of (path, element) pairs
        while queue:
            l = len(queue)
            lev = []
            for i in range(l):
                element = queue.popleft()
                lev.append(type(element))
                if hasattr(element, 'children'):  # check for leaf elements
                    for child in element.children:
                        queue.append(child)
            print(lev)
            # do stuff

    def get_nodes_to_eval(self, l):
        return self.soup.find_all(l)

    def inspect_urls(self):
        all_urls = self.soup.find_all(['a'])
        urls = [x['href'] for x in all_urls]
        a = set()
        for element in urls:
            if element.startswith('./') or element.startswith('/'):
                s = self.base+element[element.find('/'):]
                a.add(s)
            elif element.startswith('#'):
                pass
            else:
                a.add(element)

        for u in a:
            client = MongoClient(MASTER_HOST, MASTER_DB)
            database = client['dataset']
            links_collection = database['links']
            if links_collection.count_documents({'url': u}, limit=1):
                pass
            else:
                obj = {"url": u, "crawled": False}
                print('inserted', obj)
                links_collection.insert_one(obj)

    def update_current(self):
        to_find = self.url
        client = MongoClient(MASTER_HOST, MASTER_DB)
        database = client['dataset']
        links_collection = database['links']
        myquery = {"url": to_find}
        newvalues = {"$set": {"crawled": True}}
        links_collection.update_one(myquery, newvalues)

    def inspect_images(self):
        all_images = self.soup.find_all(['img'])

        for image in all_images:
            final_tags = []
            arround = str(image.parent.contents[0]).lower()
            src = str(image['src'])
            filename = str(image['src']).lower()
            try:
                altern = str(image['alt']).lower()
            except:
                altern = [None]
            for kw in self.kwords:
                if kw in arround or kw in filename or kw in altern:
                    final_tags.append(kw)
            if final_tags:
                if src.startswith('./') or src.startswith('/'):
                    filename = src[len(src)-(src[::-1].find('/')):]
                    src = self.base+src[src.find('/'):]

                data_s = {
                    "url": src,
                    "tags": final_tags,
                    "id": self.id,
                }

                client = MongoClient(MASTER_HOST, MASTER_DB)
                database = client['dataset']
                images_collection = None

                if 'images' not in database.list_collection_names():
                    print('created images')
                    images_collection = database['images']
                    images_collection.create_index("url", unique=True)

                else:
                    print('retrived')
                    images_collection = database['images']

                if images_collection.count_documents({'url': src}, limit=1):
                    pass
                else:
                    images_collection.insert_one(data_s)
                    if not os.path.exists('./images/'):
                        os.makedirs('./images/')
                    f = open('./images/'+self.id+"_"+filename, "wb")
                    print('retriving img...' + src)
                    f.write(requests.get(src).content)
                    f.close()
