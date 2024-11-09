import os
from src.webscraper.xml_parser import xmlParser

def listing_to_dictionary():
    directory = os.path.join(os.getcwd(), 'src', 'data', 'marketplace_listings')
    filenames = os.listdir(directory)
    print(filenames)
    parser = xmlParser()
    all_listings = []  # This will hold all the listing dictionaries
    for name in filenames:
        # Define keys for the dictionary
        keys = ['listing_id', 'release_id', 
                'record_name', 'artist', 
                'media_condition', 'sleeve_condition',
                'currency', 'item_price',
                'seller_name', 'seller_rating',
                'shipping_price', 'shipping_origin'
                ]
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
        listings_count = len(listing_id_values)  # Assuming all lists are the same length
        for i in range(listings_count):
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
                    shipping_origin_values
                ])
           }
            all_listings.append(listing_dict)
    return all_listings