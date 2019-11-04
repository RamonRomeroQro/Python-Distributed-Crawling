import requests
import re

class Crawler:
    def __init__(self, n_url):
        self.url=n_url
        self.images = set()
        self.links = set()

    def split(self, clients):
        pass

    def crawl_img(self):
        r = requests.get(self.url)
        for img in re.findall(r'<img.*?>', r.text):
            if '.gif' not in img: # simple filters
                self.images.add(img)

        print("\n".join(list(self.images)))

    def crawl_links(self):
        r = requests.get(self.url)
        for link in re.findall(r'<a.*>.*</a>', r.text):
            if 'href' in link:
                self.links.add(link)

        print("\n".join(list(self.links)))
        # <img src="wrongname.gif" alt="Flowers in Chania"> 
        # <a href="url">link text</a>
        

print(Crawler('http://yann.lecun.com/').crawl_img())
print(Crawler('http://yann.lecun.com/').crawl_links())

