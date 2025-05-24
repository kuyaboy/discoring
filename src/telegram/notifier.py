import os
import requests
import urllib
from src.mongodb.database import Database
from src.mongodb.queries import get_queries_from_config


from logger import get_logger
logger = get_logger()

def check_and_notify():
    mongodb = Database()
    mongodb.initialize()

    collection_listings = os.getenv('MONGODB_COLLECTION_LISTINGS')
    collection_listings_messages = os.getenv('MONGODB_COLLECTION_MESSAGES')
    chat_url = os.getenv('TELEGRAM_CHAT_URL')
    currency = os.getenv('CURRENCY')
    currency_upper = currency.upper()
    sell_item_url = 'https://www.discogs.com/sell/item/'

    queries = get_queries_from_config()
    query_results = []

    for query in queries.values():
        results = mongodb.find(collection_listings, query)
        results_list = list(results)
        query_results.extend(results_list)

    if query_results:
        for listing_id, artist_name, record_name, item_price, seller_name, seller_rating, shipping_price, shipping_origin, media_condition, sleeve_condition in zip(
                [result['listing_id'] for result in query_results],
                [result['artist'] for result in query_results],
                [result['record_name'] for result in query_results],
                [result[f'item_price_{currency}'] for result in query_results],
                [result['seller_name'] for result in query_results],
                [result['seller_rating'] for result in query_results],
                [result[f'shipping_price_{currency}'] for result in query_results],
                [result['shipping_origin'] for result in query_results],
                [result['media_condition'] for result in query_results],
                [result['sleeve_condition'] for result in query_results]
        ):

            text = f"""🚨🚨🚨*!!!ALERT!!!*🚨🚨🚨

*Artist Name:* {artist_name}
*Record Name:* {record_name}
*Seller Name:* {seller_name}
*Seller Rating (%):* {seller_rating}
*Price ({currency_upper}):* {item_price}
*Shipping Price ({currency_upper}):* {shipping_price}
*Shipping Origin:* {shipping_origin}
*Media Condition:* {media_condition}
*Sleeve Condition:* {sleeve_condition}

*Link to Record:* [Click here]({sell_item_url + listing_id})
"""

            encoded_text = urllib.parse.quote_plus(text)

            existing_entry = mongodb.find_one(collection_listings_messages, {'text': encoded_text})

            if not existing_entry:
                message_dict = {"text": encoded_text}
                mongodb.insert(collection_listings_messages, message_dict)
                requests.get(f"{chat_url}{encoded_text}", params={"parse_mode": "Markdown"})

    mongodb.close()


