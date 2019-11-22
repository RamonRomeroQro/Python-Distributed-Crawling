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

    def add_seeds(self, seeds):
        '''
        Add seed from txt file
        '''
        for l in seeds:
            l = l.strip()
            obj = {"url": l, "crawled": False}
            try:
                self.links_collection.insert_one(obj)
            except Exception as e:
                print(e)
                pass
        # aux.append(obj)

    def get_crawlable(self):
        '''
        get list of crawlables

        '''
        myquery = {"crawled": False}
        to_split = self.client['dataset']['links'].find(myquery)
        l_sendables = []
        for dictionary in to_split:
            l_sendables.append(dictionary)
        return l_sendables
