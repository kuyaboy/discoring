import os

import pymongo

from dotenv import load_dotenv

load_dotenv(override=True)

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
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_release_id(collection):
        return Database.DATABASE[collection].distinct("release_id")

    @staticmethod
    def update_one(collection, query, update):
        Database.DATABASE[collection].update_one(query, update)

    @staticmethod
    def delete_many(collection, query):
        Database.DATABASE[collection].delete_many(query)

    @staticmethod
    def delete_all_documents(collection):
        Database.DATABASE[collection].delete_many({})
