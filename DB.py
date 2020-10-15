from pymongo import MongoClient
class DB:
    def __init__(self, config):
        self.client = MongoClient(config['db']['db_server'], config['db']['db_port'])

        self.db_name = config['db']['db_name']

    def get_db(self):
        return self.client[self.db_name]

    def insert_one(self, collection, item):
        db = self.get_db()
        db[collection].update(item, item, upsert=True)

    def delete_all(self, collection):
        db = self.get_db()
        db[collection].remove({})
        
    def get_count(self, collection):
        db = self.get_db()
        return db[collection].find().count()

    def delete_last_n(self, collection, n, sort_by="creation_date"):
        db = self.get_db()
        
        ids = []

        for obj in db[collection].find().sort(sort_by, 1).limit(n):
            ids.append(obj["_id"])
        
        db[collection].remove({"_id": {"$in" : ids}})
 