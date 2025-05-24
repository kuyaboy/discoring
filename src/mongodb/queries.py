import os
import json


# this is the query template, adjust as needed. Additional parameters also have to be added to queries.json and to the function below
def create_query(artist_name: str, record_name: str, item_price_currency: int, shipping_price_currency: int, media_condition: tuple, sleeve_condition: tuple, seller_rating: float = None):
    currency = os.getenv('CURRENCY')
    query = {
        '$and': [
            {'artist': {'$eq': artist_name}},
            {'record_name': {'$eq': record_name}},
            {f'item_price_{currency}': {'$lte': item_price_currency}},
            {f'shipping_price_{currency}': {'$lte': shipping_price_currency}},
            {'media_condition': {'$in': media_condition}},
            {'sleeve_condition': {'$in': sleeve_condition}},
        ]
    }
    if seller_rating is not None:
        query['$and'].append({'seller_rating': {'$gte': seller_rating}})
    return query


# load queries from /app/src/config/query.jsopn
def get_queries_from_config(path='/app/src/config/queries.json'):
    with open(path, 'r') as f:
        query_config = json.load(f)

    queries = {}
    for query in query_config:
        for name, params in query.items():
            queries[name] = create_query(
                artist_name=params['artist_name'],
                record_name=params['record_name'],
                item_price_currency=params['item_price_currency'],
                shipping_price_currency=params['shipping_price_currency'],
                media_condition=tuple(params['media_condition']),
                sleeve_condition=tuple(params['sleeve_condition']),
                seller_rating=params.get('seller_rating') # .get since this param is only optional
            )

    return queries
