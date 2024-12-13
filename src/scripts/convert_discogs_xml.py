import json
import os
import random
import time

from webscraper.discogs_scraper import DiscogsScraper


def convert_discogs_html_to_xml():
    wantlist_path = os.path.join(os.getcwd(), 'src', 'data',
                                 'filtered_wantlist', 'filtered_wantlist.json')
    with open(wantlist_path, 'r') as file:
        wantlist = json.load(file)

    scraper = DiscogsScraper()
    scraper.get_by_release_id(wantlist)

    delay = random.uniform(2, 10)
    time.sleep(delay)
    scraper.delete_cookies()
    scraper.quit()


if __name__ == "__main__":
    convert_discogs_html_to_xml()
