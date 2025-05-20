import os

# define query template
def create_query(record_name: str, item_price_currency: int, shipping_price_currency: int, media_condition: tuple, sleeve_condition: tuple, seller_rating: float = None):
    currency = os.getenv('CURRENCY')
    query = {
        '$and': [
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

def get_queries():
    """
    Returns a dictionary of pre-defined queries.
    Use this as a template to define your own queries.

    Example:
    'my_custom_query': create_query(
        'Record Title', 100, 50,
        ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)'),
        ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)'), 95
    )

    'my_custom_query' can be anything as long as you know what this query is looking for.
    """
    return {
        'example_query': create_query(
            'Example Record', 100, 50,
            ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)'),
            ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)'), 95
        )
    }
