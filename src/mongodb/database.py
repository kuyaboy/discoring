import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.logger import get_logger

logger = get_logger()

class Database(object):
    URI = os.getenv('MONGODB_URI')
    DATABASE = None

    @staticmethod
    def initialize():
        client = MongoClient(Database.URI, server_api=ServerApi('1'))

        try:
            client.admin.command('ping')
            Database.DATABASE = client[os.getenv('MONGODB_NAME')]
            logger.info('Successfully connected to MongoDB')

        except Exception as e:
            logger.error(f'Failed to connect to MongoDB: {e}')
            raise

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert_many(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_release_id(collection):
        return Database.DATABASE[collection].distinct("release_id")

    @staticmethod
    def update_one(collection, query, update, upsert=False):
        Database.DATABASE[collection].update_one(query, update, upsert=upsert)

    @staticmethod
    def delete_many(collection, query):
        Database.DATABASE[collection].delete_many(query)

    @staticmethod
    def delete_all_documents(collection):
        Database.DATABASE[collection].delete_many({})
