import json
import os

from src.mongodb.database import Database


def update_listings_in_mongodb():
    directory = os.path.join(os.getcwd(),
                             'src', 'data',
                             'listings_json')

    collection = os.getenv('MONGODB_COLLECTION')
    filenames = os.listdir(directory)

    mongodb = Database()
    mongodb.inititalize()

    entries = []

    for file in filenames:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as listing:
            data = json.load(listing)
            data_list = list(data)
            entries.extend(data_list)

    for record in range(len(entries)):
        listing_id = entries[record]['listing_id']
        seller_name = entries[record]['seller_name']
        media_condition = entries[record]['media_condition']
        sleeve_condition = entries[record]['sleeve_condition']
        item_price_chf = entries[record]['item_price_chf']
        shipping_price_chf = entries[record]['shipping_price_chf']
        item_price = entries[record]['item_price']
        shipping_price = entries[record]['shipping_price']
        date = entries[record]['date']

        query = {
            '$and': [
                {'listing_id': {'$eq': listing_id}},
                {'seller_name': {'$eq': seller_name}},
                {
                    '$or': [
                        {'item_price': {'$ne': item_price}},
                        {'shipping_price': {'$ne': shipping_price}},
                        {'media_condition': {'$ne': media_condition}},
                        {'sleeve_condition': {'$ne': sleeve_condition}},
                    ]
                }
            ]
        }
        update = {
            '$set': {
                'item_price': item_price,
                'shipping_price': shipping_price,
                'media_condition': media_condition,
                'sleeve_condition': sleeve_condition,
                'date': date,
                'item_price_chf': item_price_chf,
                'shipping_price_chf': shipping_price_chf
            }
        }

        mongodb.update_documents(collection, query, update)


if __name__ == "__main__":
    update_listings_in_mongodb()
