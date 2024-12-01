import json
import os

from src.webscraper.discogs_scraper import DiscogsScraper


def discogs_to_xml():
    wantlist_path = os.path.join(os.getcwd(), 'src', 'data',
                                 'filtered_wantlist', 'filtered_wantlist.json')
    try:
        with open(wantlist_path, 'r') as file:
            wantlist = json.load(file)
    except FileNotFoundError:
        print("Error: wantlist.json file not found.")
        wantlist = []

    scraper = DiscogsScraper()
    try:
        scraper.get_by_release_id(wantlist)

    finally:
        scraper.delete_cookies()
        scraper.quit()


if __name__ == "__main__":
    discogs_to_xml()
