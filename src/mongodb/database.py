from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDBClient:
    def __init__(self, uri: str):

        self.uri = uri
        self.client = None

    def connect(self):

        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            # Send a ping to confirm a successful connection
            self.client.admin.command('ping')
            print(f"Pinged your deployment. You successfully connected to {self.client.list_database_names()}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_database(self, database_name: str):

        if self.client is not None:
            return self.client[database_name]
        else:
            print("Not connected to any MongoDB server.")
            return None

    def close(self):
        
        if self.client:
            self.client.close()
            print("Connection to MongoDB closed.")


if __name__ == "__main__":
    uri = os.getenv('MONGODB_URI')
    
    mongodb_client = MongoDBClient(uri=uri)
    mongodb_client.connect()

    


