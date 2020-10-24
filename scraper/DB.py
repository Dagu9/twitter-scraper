from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
import time
import sys 

class DB:
    def __init__(self, config):
        connected = False 
        server = config['db']['db_server']
        port = config['db']['db_port']

        while not connected:
            print(f"[*] Trying to connect to MongoDB server on {server}:{port} ...")
            try: 
                self.client = MongoClient(server, port, serverSelectionTimeoutMS=200)
                self.client.server_info() #test the connection

                db_name = config['db']['db_name']
                self.db = self.client[db_name]

                connected = True
                print(f"[*] Succesfully connected to MongoDB server\n")

            except ServerSelectionTimeoutError as e:
                print(f"[!] Error: No MongoDB server on {server}:{port}, retrying in 5 seconds ...\n")
                time.sleep(5)

            except ConnectionFailure as e:
                print("[!] Error: Network error, can't connect to MongoDB server, retrying in 5 seconds ...\n")
                time.sleep(5)

            except Exception as e:
                print(e)
                print("[!] Connection error, please contact the developer, exiting ...")
                sys.exit(1)

    def insert_one(self, collection, item):
        try:
            self.db[collection].update(item, item, upsert=True) #don't insert duplicates
        except Exception as e:
            print(e)
            print("[!] Insert error, please contact the developer")

    def delete_all(self, collection):
        try:
            self.db[collection].remove({})
        except Exception as e:
            print(e)
            print("[!] Delete error, please contact the developer")
        
    def get_count(self, collection):
        try:
            return self.db[collection].find().count()
        except Exception as e:
            print(e)
            print("[!] Count error, please contact the developer")

    def delete_last_n(self, collection, n, sort_by="creation_date"):

        try:
            ids = []

            for obj in self.db[collection].find().sort(sort_by, 1).limit(n):
                ids.append(obj["_id"])
            
            self.db[collection].remove({"_id": {"$in" : ids}})
        except Exception as e:
            print(e)
            print("[!] Delete N error, please contact the developer")