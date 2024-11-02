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
        year = filter_record.get('year')
        format_query = filter_record.get('format', '').lower()

        for release_id, details in wantlist.items():
            if title == details.get('title') and year == details.get('year'):
                if any(artist_query in artist_name.lower() for artist_name in details.get('artist', [])):
                    format_names = [formats.get('name', '') for formats in details.get('format', [])]
                    if any(format_query in formats.lower() for formats in format_names):
                        filtered_wantlist.append({
                            'release_id': release_id,
                            'title': details.get('title'),
                            'genre': details.get('genre'),
                            'artist': details.get('artist'),
                            'year': details.get('year'),
                            'format': format_names,
                            **details
                        })
                    
    return filtered_wantlist
