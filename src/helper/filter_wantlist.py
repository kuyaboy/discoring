import os
import json

from src.discogsclient.wantlist import DiscogsWantlistClient


def wantlist_filter():
    
    discogs_client = DiscogsWantlistClient()
    wantlist = discogs_client.get_wantlist()

    filter_config_path = os.path.join(os.getcwd(), 'src', 'config', 'wantlist_filter_config.json')
    with open(filter_config_path, 'r') as file:
        filter_criteria = json.load(file)
    
    filtered_wantlist = []
    
    for filter_record in filter_criteria:
        artist_query = filter_record.get('artist', '').lower()
        title = filter_record.get('title')

        for release_id, details in wantlist.items():
            if title == details.get('title'):
                if any(artist_query in artist_name.lower() for artist_name in details.get('artist', [])):
                    filtered_wantlist.append({
                        'release_id': release_id,
                        'title': details.get('title'),
                        'artist': details.get('artist'),
                        **details
                    })
                    
    return filtered_wantlist