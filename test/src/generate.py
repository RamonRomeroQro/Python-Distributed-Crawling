import os

def generate_html(list_tuples, dataset):
    to_link=3
    current=0
    indexing=1
    while indexing<len(list_tuples):
        nf=open(list_tuples[current][0], 'w')
        info=dataset[list_tuples[current][1]]
        block=[]
        for k,v in info:
            s=f"{k} : {v}"
            block.append(s)
        block="<br>".join(block)
        links=[]
        c=0
        while indexing<len(list_tuples):
            links.append((list_tuples[indexing][0], list_tuples[indexing][3]))
            c+=1
            indexing+=1
            if c==to_link:
                break
        links_html=[]
        for t in links:
            s=f'<a href="{t[0]}"> {t[1]} </a>'
            links_html.append(s)
        links_html="".join(links_html)

        my_html=f"""
        <!doctype html>
        <html>
        <head>
            <title>{list_tuples[current][3]}</title>
        </head>
        <body>
            <div>
            {
                block
            }

             <img src="{list_tuples[current][2]}"  height="100" > 
            
            </div>
            <div>
            {
                links_html
            }            
            </div>
        </body>
        </html>
        """
        print(my_html)

        current+=1

def main():
    im_folder="./images/"
    images=os.listdir(im_folder)
    uniques_images=set()
    all_names_html=[]
    for name in images:
        
        i=len(name)-1
        while(i>=0):
            if name[i]=='_':
                aux=name[:i]
                # print('>>>', name)
                # if aux=='Albrecht_Dürer':
                #     n= 'Albrecht_Dürer'
                #     os.rename(im_folder+name,im_folder+n+name[i:])
                title=name[:name.find('.')]
                html_name=title+".html" #file to gen
                all_names_html.append((html_name, aux, im_folder+name, title))
                uniques_images.add(aux)
                break
            i-=1

    # print(uniques_images) 
    f=open("./artists.csv", 'r')
    classes=[]
    rows={}
    for index, line in enumerate(f):
        if index==0:
            classes=line.strip().split(',')
        else:
            data=line.strip().split(',')
            d_element={}
            for i,c in enumerate(classes):
                d_element[c]=data[i]
            rows["_".join(data[1].split(' '))]=d_element
    f.close()
    generate_html(all_names_html, rows)
    # a=list(sorted(rows.keys()))
    # b=list(sorted(list(uniques_images)))
    # print('>>',a)
    # print('>>',b)
    # print('>>>', b[0]==a[0])
    # print(set(rows.keys())-uniques_images)
    # print(uniques_images-set(rows.keys()))

if __name__ == "__main__":
    main()