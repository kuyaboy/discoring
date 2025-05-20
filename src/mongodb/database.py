import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.logger import get_logger

logger = get_logger()

class Database:
    client = None
    db = None

    @staticmethod
    def initialize():
        try:
            Database.client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
            Database.client.admin.command('ping')
            Database.db = Database.client[os.getenv('MONGODB_NAME')]
            logger.info('Successfully connected to MongoDB')
        except Exception as e:
            logger.error(f'Failed to connect to MongoDB: {e}')
            raise

    @staticmethod
    def insert(collection, data):
        Database.db[collection].insert_one(data)

    @staticmethod
    def find(collection, query):
        return Database.db[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.db[collection].find_one(query)

    @staticmethod
    def find_release_id(collection):
        return Database.db[collection].distinct("release_id")

    @staticmethod
    def update_one(collection, query, update, upsert=False):
        Database.db[collection].update_one(query, update, upsert=upsert)

    @staticmethod
    def delete_many(collection, query):
        Database.db[collection].delete_many(query)

    @staticmethod
    def delete_all_documents(collection):
        Database.db[collection].delete_many({})
        logger.info(f'Deleted all documents from {collection}')

    @staticmethod
    def close():
        if Database.client:
            Database.client.close()
            logger.info('Successfully closed connection to MongoDB')
