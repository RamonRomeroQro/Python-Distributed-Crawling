from bs4 import BeautifulSoup
from collections import deque
import requests
# import re

class Crawler:
    def __init__(self, n_url):
        self.url=n_url
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, features="html.parser")
    
    def beautiful(self):
        return self.soup.prettify()
    def bfs(self):
        queue = deque([self.soup]) # queue of (path, element) pairs
        while queue:
            l=len(queue)
            lev=[]
            for i in range(l):
                element = queue.popleft()
                lev.append(type(element))
                if hasattr(element, 'children'):  # check for leaf elements
                    for child in element.children:
                        queue.append(child)
            print(lev)
            # do stuff
            

print(Crawler("http://yann.lecun.com/").bfs())

    # def split(self, clients):
    #     pass

    # def crawl_img(self):
    #     r = requests.get(self.url)
    #     for img in re.findall(r'<img.*?>', r.text):
    #         if '.gif' not in img: # simple filters
    #             self.images.add(img)

    #     print("\n".join(list(self.images)))

    # def crawl_links(self):
    #     r = requests.get(self.url)
    #     for link in re.findall(r'<a.*>.*</a>', r.text):
    #         if 'href' in link:
    #             self.links.add(link)

    #     print("\n".join(list(self.links)))
    #     # <img src="wrongname.gif" alt="Flowers in Chania"> 
    #     # <a href="url">link text</a>
