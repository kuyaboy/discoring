import os
import requests
import urllib
from mongodb.database import Database
from mongodb.queries import get_query_les_nubiennes
from mongodb.queries import get_query_return_of_the_devils_son
from mongodb.queries import get_query_roads_out_the_ghetto
from mongodb.queries import get_query_sun_kissed_lady


def check_and_notify():
    mongodb = Database()
    mongodb.inititalize()

    collection = os.getenv('MONGODB_COLLECTION')
    chat_url = os.getenv('TELEGRAM_CHAT_URL')
    sell_item_url = 'https://www.discogs.com/sell/item/'

    queries = [
        get_query_les_nubiennes,
        get_query_return_of_the_devils_son,
        get_query_roads_out_the_ghetto,
        get_query_sun_kissed_lady
    ]

    query_results = []

    for get_query in queries:
        query = get_query()
        results = mongodb.find(collection, query)
        results_list = list(results)
        query_results.extend(results_list)

    if query_results:
        for listing_id, record_name, record_price, shipping_price, media_condition, sleeve_condition in zip(
                [result['listing_id'] for result in query_results],
                [result['record_name'] for result in query_results],
                [result['item_price_chf'] for result in query_results],
                [result['shipping_price_chf'] for result in query_results],
                [result['media_condition'] for result in query_results],
                [result['sleeve_condition'] for result in query_results]
        ):

            text = f"""🚨🚨🚨*!!!ALERT!!!*🚨🚨🚨

*Record Name:* {record_name}
*Price (CHF):* {record_price}
*Shipping Price (CHF):* {shipping_price}
*Media Condition:* {media_condition}
*Sleeve Condition:* {sleeve_condition}

*Link to Record:* [Click here]({sell_item_url + listing_id})
"""

            encoded_text = urllib.parse.quote_plus(text)

            requests.get(f"{chat_url}{encoded_text}", params={"parse_mode": "Markdown"})


