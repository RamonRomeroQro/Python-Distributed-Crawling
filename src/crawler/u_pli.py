
# begin
# morelinks_to_seed
# iteraten



from pymongo import MongoClient

class CrawClient():
    def __init__(self, ip_v, port_v):    
        self.client = MongoClient(ip_v, port_v)
        self.database=None
        self.links_collection=None
        if "dataset" in self.client.list_database_names():
            self.database=self.client['dataset']
        
        else:
            print('created db')
            self.database=self.client['dataset']

        if 'links' not in self.database.list_collection_names():
            print('created links')
            self.links_collection=self.database['links']
            self.links_collection.create_index("url", unique=True)
    
        else:
            print ('retrived')
            self.links_collection=self.database['links']
    
    def add_seeds(self, path='./seeds.txt'):
        seed_p=open(path, 'r')
        for l in seed_p:
            l=l.strip()
            obj={"url":l, "crawled":False}
            try:
                self.links_collection.insert_one(obj)
            except:
                pass
        seed_p.close()
            #aux.append(obj)

    def sed_to_crawl(self, connections_array):
        myquery = { "crawled":False }
        to_split = self.client['dataset']['dataset']['links'].find(myquery)
        # for link in to_split:

    


def main():
    play()
    return -1
if __name__ == "__main__":
    main()



