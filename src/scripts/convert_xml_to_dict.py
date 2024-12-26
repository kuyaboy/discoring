import os
import json

from datetime import datetime

from logger import get_logger
from webscraper.xml_parser import xmlParser

logger = get_logger()

def convert_wantlist_xml_to_dict():
    directory = os.path.join(os.getcwd(),
                             'src', 'data',
                             'marketplace_listings')

    output_directory = os.path.join(os.getcwd(),
                                    'src', 'data',
                                    'listings_json')

    filenames = os.listdir(directory)

    if len(filenames) < 1:
        logger.error(f'Something went wrong. No files in: {directory}')
        raise FileNotFoundError(f"No files were found in the directory: {directory}")

    parser = xmlParser()

    # Define keys
    keys = ['listing_id', 'release_id',
            'record_name', 'artist',
            'media_condition', 'sleeve_condition',
            'currency', 'item_price',
            'seller_name', 'seller_rating',
            'shipping_price', 'shipping_origin', 'date']

    for name in filenames:
        # Get the list values from parser
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

        # Check if all lists are of the same length otherwise something with the parsing went wrong
        lengths = [
            len(listing_id_values), len(release_id_values),
            len(record_name_values), len(artist_name_values),
            len(media_condition_values), len(sleeve_condition_values),
            len(currency_values), len(item_price_values),
            len(seller_name_values), len(seller_rating_values),
            len(shipping_price_values), len(shipping_origin_values)
        ]

        if len(set(lengths)) > 1:
            error_msg = f"Lists of {name} don't have the same lengths. Check .xml file " \
                        f"Lengths: {lengths}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Build the listings if lengths are the same
        listings = []
        listings_count = len(listing_id_values)  # All lists should have the same length
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
