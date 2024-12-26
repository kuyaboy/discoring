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
        'princesses_nubiennes': create_query('Princesses Nubiennes', 60, 20),
        'how_it_go_1_life_2_live': create_query('How It Go! (Da Remix) / 1 Life 2 Live', 20, 10),
        'sun_kissed_lady': create_query('Sun Kissed Lady', 45, 15),
        'two_roads_out_the_ghetto': create_query('2 Roads Out The Ghetto', 80, 20),
        'the_lp': create_query('The LP', 60, 20),
        'bossaline': create_query('Bossaline', 50, 20),
        'grand_puba_2000': create_query('2000', 30, 15),
        'werd_of_mouph': create_query('Werd of Mouph', 30, 15),
        'ego_trippin': create_query('Ego Trippin', 30, 15),
        'takin_mine': create_query('Takin Mine', 50, 15),
    }
