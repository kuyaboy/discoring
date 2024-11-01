import json
import os

import src.helper.filter_wantlist

def filtered_wantlist_to_json():
    
    filtered_wantlist = 
    
    new_json_path = os.path.join(os.getcwd(), 'src', 'data', 'filtered_wantlist.json')
    
    with open(new_json_path, 'w') as jsonFile:
        json.dump(scrapedData, jsonFile)