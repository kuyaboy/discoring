import os
import json
from mongodb.database import Database  # Assuming you have a Database class handling MongoDB connections

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

            existing_entry = mongodb.find_one(collection, {'listing_id': listing_id, 'seller_name': seller_name})

            if existing_entry:
                # Check if any of the relevant fields have changed from the collection compared to the new dictionary
                if (existing_entry.get('item_price') != record['item_price'] or
                    existing_entry.get('shipping_price') != record['shipping_price'] or
                    existing_entry.get('media_condition') != record['media_condition'] or
                    existing_entry.get('sleeve_condition') != record['sleeve_condition']):

                    # Update the document only if a field has changed
                    update_query = {'listing_id': listing_id, 'seller_name': seller_name}
                    update_data = {'$set': record}

                    mongodb.update_one(collection, update_query, update_data, upsert=True)

if __name__ == "__main__":
    update_listings_in_mongodb()
