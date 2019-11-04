from pymongo import MongoClient


class DataManager():
    def __init__(self, ip_v, port_v, num):
        ''' 
        Initialize using ip and port to connect to database (crate db instances)
        '''
        self.client = MongoClient(ip_v, port_v)
        self.split_num = num

        self.database = None
        self.links_collection = None
        if "dataset" in self.client.list_database_names():
            self.database = self.client['dataset']

        else:
            print('created db')
            self.database = self.client['dataset']

        if 'links' not in self.database.list_collection_names():
            print('created links')
            self.links_collection = self.database['links']
            self.links_collection.create_index("url", unique=True)

        else:
            print('retrived')
            self.links_collection = self.database['links']

    def add_seeds(self, path='./seeds.txt'):
        '''
        Add seed from txt file
        '''
        seed_p = open(path, 'r')
        for l in seed_p:
            l = l.strip()
            obj = {"url": l, "crawled": False}
            try:
                self.links_collection.insert_one(obj)
            except:
                pass
        seed_p.close()
        # aux.append(obj)

    def get_crawlable(self):
        '''
        get matrix of crawlables

        '''
        myquery = {"crawled": False}
        to_split = self.client['dataset']['dataset']['links'].find(myquery)
        # for link in to_split:
        matrix_sendables = [[] for x in range(self.split_num)]
        for i, dictionary in enumerate(to_split):
            matrix_sendables[i % self.split_num].append(dictionary)
        return matrix_sendables
