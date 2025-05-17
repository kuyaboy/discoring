#!/opt/venv/bin/python3
import json
import os

from dotenv import load_dotenv
load_dotenv()

from src.logger import get_logger
from src.helper.filter_wantlist import wantlist_filter

logger = get_logger()

def sync_filtered_wantlist_to_json(filtered_wantlist):
    wantlist_export = filtered_wantlist
    new_json_path = os.path.join(os.getcwd(), 'src', 'data', 'filtered_wantlist')

    if not os.path.exists(new_json_path):
        os.makedirs(new_json_path)

    json_file_path = os.path.join(new_json_path, 'wantlist.json')

    with open(json_file_path, 'w') as jsonFile:
        json.dump(wantlist_export, jsonFile, indent=3)


if __name__ == "__main__":
    logger.debug('Attempting to sync wantlist')
    wantlist = wantlist_filter()
    sync_filtered_wantlist_to_json(wantlist)
    logger.info('Successfully synced wantlist')
