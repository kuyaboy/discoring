import os
import json
from src.discogsclient.wantlist import DiscogsWantlistClient

def wantlist_filter():
    discogs_client = DiscogsWantlistClient()
    wantlist = discogs_client.get_wantlist()

    filter_config_path = os.path.join(os.getcwd(), 'src', 'config', 'wantlist_filter_config.json')
    with open(filter_config_path, 'r') as file:
        filter_config = json.load(file)

    filtered = []

    for record in wantlist:
        info = record.get("basic_information", {})
        release_id = info.get("id")
        title = info.get("title", "")
        year = info.get("year")
        genres = info.get("genres", [])
        formats = [fmt.get("name", "") for fmt in info.get("formats", [])]
        artists = [artist.get("name", "") for artist in info.get("artists", [])]

        for f in filter_config:
            f_artist = f.get("artist", "").lower()
            f_title = f.get("title", "").lower()
            f_year = f.get("year")
            f_format = f.get("format", "").lower()

            if (
                (not f_artist or any(a.lower() == f_artist for a in artists)) and
                (not f_title or title.lower() == f_title) and
                (f_year is None or year == f_year) and
                (not f_format or any(fmt.lower() == f_format for fmt in formats))
            ):
                filtered.append({
                    "release_id": release_id,
                    "artist": artists,
                    "title": title,
                    "year": year,
                    "format": formats,
                    "genre": genres
                })
                break

    return filtered


