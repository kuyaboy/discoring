#!/opt/venv/bin/python3
import os

from dotenv import load_dotenv
load_dotenv()

from src.mongodb.database import Database


def empty_collection(collection: str):

    collection = os.getenv(collection)

    mongodb = Database()
    mongodb.initialize()
    mongodb.delete_all_documents(collection)
    mongodb.close()

if __name__ == "__main__":
    empty_collection('MONGODB_COLLECTION_MESSAGES')
