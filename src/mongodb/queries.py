# define query template
def create_query(record_name, item_price_chf, shipping_price_chf):
    return {
        '$and': [
            {'record_name': {'$eq': record_name}},
            {'item_price_chf': {'$lte': item_price_chf}},
            {'shipping_price_chf': {'$lte': shipping_price_chf}},
            {'media_condition': {'$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}},
            {'sleeve_condition': {'$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}},
        ]
    }

def get_queries():
    return {
        'princesses_nubiennes': create_query('Princesses Nubiennes', 80, 80),
        'butter_smoother': create_query('今すぐ欲しい', 45, 15)
    }
