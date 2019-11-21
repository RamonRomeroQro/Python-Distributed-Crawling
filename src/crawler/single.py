import struct
import json
import requests
import pickle
import sys
import re
from bs4 import BeautifulSoup
from collections import deque
import requests
from collections import deque


f = open('./../settings.json')
settings = json.load(f)
f.close()

NUM_SLAVES = len(settings['slaves'])
MASTER_HOST = settings['master']['ip']  # The server's hostname or IP address
MASTER_PORT = settings['master']['port']        # The port used by the server
MASTER_DB = settings['master']['db']        # The port used by the server
KWORDS = set(settings['kwords'])
SEEDS = list(set(settings['seeds']))


def g_base(url):
    c=0
    for i,e in enumerate(url):
        if e=='/':
            c+=1
        if c==3:
            return i
    return len(url)

def main():
    images_db={}
    visited=set()
    id_v='single'
    q=deque(list(SEEDS))
    while q:
        seed = q.popleft()
        visited.add(seed)
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

                if src not in images_db:
                    images_db[src] = {
                        "tags": final_tags,
                        "id": id_v,
                    }
                    f = open('./images/'+id_v+"_"+filename, "wb")
                    print('retriving img...' + src)
                    f.write(requests.get(src).content)
                    f.close()
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

        # print('AAA>>', a)
        # print('AAA>>', base)

        for u in a:
            if u not in visited:
                print("Inserted "+ u)
                q.append(u)


if __name__ == "__main__":
    main()