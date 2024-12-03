import os

import pymongo


class Database(object):
    URI = os.getenv('MONGODB_URI')
    DATABASE = None

    @staticmethod
    def inititalize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client[os.getenv('MONGODB_NAME')]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert_many(data)

    @staticmethod
    def find_deals(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def delete_all_documents(collection):
        Database.DATABASE[collection].delete_many({})

