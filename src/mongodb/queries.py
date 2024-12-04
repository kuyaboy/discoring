def get_query_les_nubiennes():
    return {
        '$and': [
            {'record_name': {'$eq': 'Princesses Nubiennes'}},
            {'item_price_chf': {'$lte': 100 }},
            {'shipping_price_chf': {'$lte': 100}},
            {
                '$or': [
                    {'media_condition': {
                        '$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}},
                    {'sleeve_condition': {
                        '$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}}
                ]
            }
        ]
    }

def get_query_return_of_the_devils_son():
    return {
        '$and': [
            {'record_name': {'$eq': 'Return Of The Devils Son'}},
            {'item_price_chf': {'$lte': 100 }},
            {'shipping_price_chf': {'$lte': 100}},
            {
                '$or': [
                    {'media_condition': {
                        '$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}},
                    {'sleeve_condition': {
                        '$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}}
                ]
            }
        ]
    }

def get_query_roads_out_the_ghetto():
    return {
        '$and': [
            {'record_name': {'$eq': '2 Roads Out The Ghetto'}},
            {'item_price_chf': {'$lte': 100 }},
            {'shipping_price_chf': {'$lte': 100}},
            {
                '$or': [
                    {'media_condition': {
                        '$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}},
                    {'sleeve_condition': {
                        '$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}}
                ]
            }
        ]
    }

def get_query_sun_kissed_lady():
    return {
        '$and': [
            {'record_name': {'$eq': 'Sun Kissed Lady'}},
            {'item_price_chf': {'$lte': 100 }},
            {'shipping_price_chf': {'$lte': 100}},
            {
                '$or': [
                    {'media_condition': {
                        '$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}},
                    {'sleeve_condition': {
                        '$in': ('Very Good Plus (VG+)', 'Near Mint (NM or M-)', 'Mint (M)')}}
                ]
            }
        ]
    }
