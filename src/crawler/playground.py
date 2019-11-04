from pymongo import MongoClient

def play():
    client = MongoClient()
    client = MongoClient('127.0.0.1', 6000)
    db = client['dataset']
    imagenes = db['images']
    links = db['links']

def main():
    play()
    return -1
if __name__ == "__main__":
    main()