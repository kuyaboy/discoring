import os
import json
from src.discogsclient.wantlist import DiscogsWantlistClient

def wantlist_filter():
    # Initialize Discogs client and get the wantlist
    discogs_client = DiscogsWantlistClient()
    wantlist = discogs_client.get_wantlist()

    filter_config_path = os.path.join(os.getcwd(), 'src', 'config', 'wantlist_filter_config.json')

    with open(filter_config_path, 'r') as file:
        filter_criteria = json.load(file)

    filtered_wantlist = []

    # Loop through each filter record in the config
    for filter_record in filter_criteria:
        artist_query = filter_record.get('artist', '').lower()
        title = filter_record.get('title', '').lower()
        year = filter_record.get('year')
        format_query = filter_record.get('format', '').lower()
        country = filter_record.get('country', '').lower()

        # Loop through the wantlist from Discogs
        for release_id, details in wantlist.items():
            if (title == details.get('title', '').lower() and
                year == details.get('year') and
                country == details.get('country', '').lower()):

                # Check if the artist matches the filter criteria
                artist_names = [artist.lower() for artist in details.get('artist', [])]
                if any(artist_query in artist for artist in artist_names):
                    format_names = [formats.get('name', '').lower() for formats in details.get('format', [])]
                    if any(format_query in format for format in format_names):
                        filtered_wantlist.append({
                            'release_id': release_id,
                            'title': details.get('title'),
                            'genre': details.get('genre'),
                            'artist': details.get('artist'),
                            'year': details.get('year'),
                            'country': details.get('country'),
                            'format': format_names,
                            **details
                        })

    return filtered_wantlist
