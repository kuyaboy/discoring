import json
import os
from mongodb.database import Database

from src.logger import get_logger
logger = get_logger()

def delete_orphaned_documents():
    directory = os.path.join(os.getcwd(), 'src', 'data', 'listings_json')
    filenames = os.listdir(directory)

    collection = os.getenv('MONGODB_COLLECTION')
    mongodb = Database()
    mongodb.inititalize()

    new_listing_ids = set()

    for file in filenames:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as listing:
            data = json.load(listing)
            data_list = list(data)

            for record in data_list:
                new_listing_ids.add(record['listing_id'])

    query = {'listing_id': {'$nin': list(new_listing_ids)}}

    orphaned_documents = list(mongodb.find(collection, query))
    if orphaned_documents:
        for doc in orphaned_documents:
            logger.debug(f'The following document will get deleted: {doc}')

        mongodb.delete_many(collection, query)
        logger.info(f"Deleted orphaned documents from MongoDB.")

    else:
        logger.info('No orphaned documents found')

if __name__ == "__main__":
    delete_orphaned_documents()
