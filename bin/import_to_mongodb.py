#!/opt/venv/bin/python3
import json
import os

from dotenv import load_dotenv
load_dotenv()

from src.mongodb.database import Database


def import_listings_to_mongodb():
    directory = os.path.join(os.getcwd(),
                             'src', 'data',
                             'listings_json')

    collection = os.getenv('MONGODB_COLLECTION')
    filenames = os.listdir(directory)
    print(filenames)

    mongodb = Database()
    mongodb.inititalize()
    mongodb.delete_all_documents(collection)

    for file in filenames:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as listing:
            data = json.load(listing)
        mongodb.insert(collection, data)


if __name__ == "__main__":
    import_listings_to_mongodb()
