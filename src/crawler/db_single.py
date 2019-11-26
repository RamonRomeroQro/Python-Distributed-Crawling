import requests
import re
from bs4 import BeautifulSoup
import requests
import os
import json
from pymongo import MongoClient

f = open('./../settings.json')
settings = json.load(f)
f.close()

NUM_SLAVES = settings['slaves']
MASTER_HOST = settings['master']['ip']  # The server's hostname or IP address
MASTER_PORT = settings['master']['port']        # The port used by the server
MASTER_DB = settings['master']['db']        # The port used by the server
KWORDS = set(settings['kwords'])
SEEDS = list(set(settings['seeds']))
MXDEPTH= settings['depth']
DOWNLOAD = settings['force_downlooad']


def g_base(url):
    c = 0
    for i, e in enumerate(url):
        if e == '/':
            c += 1
        if c == 3:
            return i
    return len(url)


def main():
    client = MongoClient(MASTER_HOST, MASTER_DB)
    database = None
    links_collection = None
    if "dataset" not in client.list_database_names():
        print('created db')
    database = client['dataset']

    if 's_links' not in database.list_collection_names():
        print('created links')
        links_collection = database['s_links']
        links_collection.create_index("url", unique=True)

    else:
        print('retrived')
        links_collection = database['s_links']
    for l in SEEDS:
        l = l.strip()
        obj = {"url": l, "crawled": False}
        try:
            links_collection.insert_one(obj)
        except Exception as e:
            print(e)
            pass

    current_level = 0

    while links_collection.count_documents({'crawled': False}, limit=1):
        print('crawl')

        myquery = {"crawled": False}
        to_split = links_collection.find(myquery)
        l_sendables = []
        for dictionary in to_split:
            l_sendables.append(dictionary)

        for d in l_sendables:
            seed = d['url']
            r = requests.get(seed)
            base = seed[:g_base(seed)]
            soup = BeautifulSoup(r.text, features="html.parser")
            ####################
            ####################
            ####################
            all_images = soup.find_all(['img'])

            for image in all_images:
                final_tags = []
                arround = str(image.parent.contents[0]).lower()
                src = str(image['src'])
                filename = str(image['src']).lower()
                try:
                    altern = str(image['alt']).lower()
                except:
                    altern = [None]
                for kw in KWORDS:
                    #print('>>>', kw, arround , filename , altern)
                    if kw in arround or kw in filename or kw in altern:
                        final_tags.append(kw)
                if final_tags:
                    if src.startswith('./') or src.startswith('/'):
                        filename = src[len(src)-(src[::-1].find('/')):]
                        src = base+src[src.find('/'):]

                    data_s = {
                        "url": src,
                        "tags": final_tags,
                        "id": "single",
                    }


                    images_collection = None

                    if 's_images' not in database.list_collection_names():
                        print('created images')
                        images_collection = database['s_images']
                        images_collection.create_index("url", unique=True)

                    else:
                        print('retrived')
                        images_collection = database['s_images']

                    if images_collection.count_documents({'url': src}, limit=1):
                        pass
                    else:
                        images_collection.insert_one(data_s)
                        if DOWNLOAD:
                            if not os.path.exists('./images/'):
                                os.makedirs('./images/')
                            f = open('./images/'+"single"+"_"+filename, "wb")
                            print('retriving img...' + src)
                            f.write(requests.get(src).content)
                            f.close()
                        pass

            #########
            ########
            ######
            all_urls = soup.find_all(['a'])
            urls = [x['href'] for x in all_urls]
            a = set()

            for element in urls:
                if element.startswith('./') or element.startswith('/'):
                    s = base+element[element.find('/'):]
                    a.add(s)
                elif element.startswith('#'):
                    pass
                else:
                    a.add(element)

            for u in a:
                if links_collection.count_documents({'url': u}, limit=1):
                    pass
                else:
                    obj = {"url": u, "crawled": False}
                    #print('inserted', obj)
                    links_collection.insert_one(obj)

            #####

            myquery = {"url": seed}
            newvalues = {"$set": {"crawled": True}}
            links_collection.update_one(myquery, newvalues)

        print("level")
        current_level+=1
        if current_level == MXDEPTH:
            break


if __name__ == "__main__":
    main()
