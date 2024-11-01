import json
import os

from src.helper.filter_wantlist import wantlist_filter

def filtered_wantlist_to_json(filtered_wantlist):
    
    wantlist_export = filtered_wantlist
    
    new_json_path = os.path.join(os.getcwd(), 'src', 'data', 'filtered_wantlist', 'filtered_wantlist.json')
    
    with open(new_json_path, 'w') as jsonFile:
        json.dump(wantlist_export, jsonFile, indent = 3)
        
if __name__ == "__main__":
    wantlist = wantlist_filter()
    filtered_wantlist_to_json(wantlist)