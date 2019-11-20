from bs4 import BeautifulSoup
import requests
url="http://0.0.0.0:8000"
r = requests.get(url)
soup = BeautifulSoup(r.text, features="html.parser")


kwords=['smile']
all_images= soup.find_all(['img'])

for image in all_images:
    final_tags=[]
    arround=str(image.parent.contents[0]).lower()
    src=str(image['src'])
    filename=str(image['src']).lower()
    altern=str(image['alt']).lower()
    for kw in kwords:
        if kw in arround or kw in filename or  kw in altern:
            final_tags.append(kw) 
    if final_tags:
        if src.startswith('./') or src.startswith('/') :
            filename=src[len(src)-(src[::-1].find('/')):]
            src=url+src[src.find('/'):]

        data_s={
            "retrived": src,
            "tags": final_tags,
            "socket": ("0.0.0.0", 7001)
        }
        print(data_s)
        with open('./images/'+filename, "wb") as f:
            f.write(requests.get(src).content)

