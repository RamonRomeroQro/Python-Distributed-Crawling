
# begin
# morelinks_to_seed
# iteraten



from pymongo import MongoClient

def play():
    client = MongoClient('127.0.0.1', 7050)
    db_list = client.list_database_names()
    database=None
    links_collection=None
    if "dataset" in db_list:
        database=client['dataset']
       

    else:
        print('created db')
        database=client['dataset']

    if 'links' not in database.list_collection_names():
        print('created links')
        links_collection=database['links']
        links_collection.create_index("url", unique=True)
  
    else:
        print ('retrived')
        links_collection=database['links']

    
    seed_p=open('./seeds.txt', 'r')
    aux=[]
    for l in seed_p:
        l=l.strip()
        obj={"url":l, "crawled":False}
        try:
            links_collection.insert_one(obj)
        except:
            pass
        #aux.append(obj)

    if aux:
        print('seeds Added')
        links_collection.insert_many(aux)



    myquery = { "crawled":False }
    to_split = list(links_collection.find(myquery))
    
    print(type((to_split)))
    print(((to_split)))
    CONSTANT=2
    a=(len(to_split))/CONSTANT
    for i in range(CONSTANT):
        if i!= CONSTANT-1:
            conexion[k].sendall(to_split[(a*i):(a*(i+1))])
        else:
            conexion[k].sendall(to_split[(a*i):])



def main():
    play()
    return -1
if __name__ == "__main__":
    main()



