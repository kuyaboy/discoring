import os
import json

from datetime import datetime

from src.webscraper.xml_parser import xmlParser


def convert_wantlist_xml_to_dict():
    directory = os.path.join(os.getcwd(),
                             'src', 'data',
                             'marketplace_listings')

    output_directory = os.path.join(os.getcwd(),
                                    'src', 'data',
                                    'listings_json')

    filenames = os.listdir(directory)
    parser = xmlParser()

    for name in filenames:
        keys = ['listing_id', 'release_id',
                'record_name', 'artist',
                'media_condition', 'sleeve_condition',
                'currency', 'item_price',
                'seller_name', 'seller_rating',
                'shipping_price', 'shipping_origin','date']

        # Use the parser methods to get lists of values
        listing_id_values = parser.get_listing_id(name)
        release_id_values = parser.get_release_id(name)
        record_name_values = parser.get_record_name(name)
        artist_name_values = parser.get_artist_name(name)
        media_condition_values = parser.get_media_condition(name)
        sleeve_condition_values = parser.get_sleeve_condition(name)
        currency_values = parser.get_currency(name)
        item_price_values = parser.get_item_price(name)
        seller_name_values = parser.get_seller_name(name)
        seller_rating_values = parser.get_seller_rating(name)
        shipping_price_values = parser.get_shipping_price(name)
        shipping_origin_values = parser.get_shipping_origin(name)

        # Build the listings
        listings = []
        listings_count = len(listing_id_values)
        for i in range(listings_count):

            current_date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            listing_dict = {
                keys[j]: values[i] for j, values in enumerate([
                    listing_id_values,
                    release_id_values,
                    record_name_values,
                    artist_name_values,
                    media_condition_values,
                    sleeve_condition_values,
                    currency_values,
                    item_price_values,
                    seller_name_values,
                    seller_rating_values,
                    shipping_price_values,
                    shipping_origin_values,
                ])
            }

            listing_dict['date'] = current_date
            listings.append(listing_dict)

            release_id = listing_dict.get('release_id', 'unknown')
            json_filename = f"{release_id}.json"
            json_filepath = os.path.join(output_directory, json_filename)
            with open(json_filepath, 'w', encoding='utf-8') as json_file:
                json.dump(listings, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    convert_wantlist_xml_to_dict()
