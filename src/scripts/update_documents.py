import os
import json
from mongodb.database import Database
from logger import get_logger

logger = get_logger()

def update_listings_in_mongodb():
    directory = os.path.join(os.getcwd(), 'src', 'data', 'listings_json')

    collection = os.getenv('MONGODB_COLLECTION')
    filenames = os.listdir(directory)

    mongodb = Database()
    mongodb.initialize()

    for file in filenames:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as listing:
            data = json.load(listing)

        for record in data:
            listing_id = record['listing_id']
            seller_name = record['seller_name']
            record_name = record['record_name']

            existing_entry = mongodb.find_one(collection, {'listing_id': listing_id, 'seller_name': seller_name})

            if existing_entry:
                logger.info('')
                # Check if any of the relevant fields have changed from the collection compared to the new dictionary
                if (existing_entry.get('item_price') != record.get('item_price') or
                    existing_entry.get('shipping_price') != record.get('shipping_price') or
                    existing_entry.get('media_condition') != record.get('media_condition') or
                    existing_entry.get('sleeve_condition') != record.get('sleeve_condition')):

                    # Update the document only if a field has changed
                    update_query = {'listing_id': listing_id, 'seller_name': seller_name}
                    update_data = {'$set': record}
                    logger.debug(f'Updating: {record}')
                    mongodb.update_one(collection, update_query, update_data, upsert=True)
                    logger.info(f'Successfully updated: {record}')

                else:
                    logger.info(f'No listings to update for {record_name} with listing_id: {listing_id}')

            else:
                mongodb.insert(collection, record)
                logger.info(f'Added new entry for: {record["record_name"]}')


if __name__ == "__main__":
    update_listings_in_mongodb()
