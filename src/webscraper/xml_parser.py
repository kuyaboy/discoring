import os
import regex as re

class xmlParser:
    def __init__(self):
            self.root = None

    def load_xml_file(self, file_name):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, 'src', 'data', 'raw', file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()  # Return the content of the file
    
    def get_listing_id(self, file_name):
        xml_file = self.load_xml_file(file_name)
        
        # Define the regex pattern to find the release IDs and titles
        listing_pattern = r'<td class="item_description">.*?<a href="/sell/item/(\d+)"[^>]*>'
        
        # Find all matches in the XML content
        listing_ids = re.findall(listing_pattern, xml_file, re.DOTALL)
        
        if listing_ids:
            print(f'Found {len(listing_ids)} instances for listing ID')
            return listing_ids
        else:
            print('No Matches for release_id')
            return None
        
    def get_release_id(self, file_name):
        xml_file = self.load_xml_file(file_name)
        
        # Define the regex pattern to find the release IDs and titles
        release_pattern = r'<a href="/release/(\d+)-[^"]*" class="item_release_link hide_mobile">View Release Page<\/a>'
        
        # Find all matches in the XML content
        release_ids = re.findall(release_pattern, xml_file, re.DOTALL)
        
        if release_ids:
            print(f'Found {len(release_ids)} instances for release ID')
            return release_ids
        else:
            print('No Matches for release_id')
            return None
    
    def get_artist_name(self, file_name):
        
        xml_file = self.load_xml_file(file_name)
        
        artist_name_pattern = r'<td class="item_description">.*?<a href="/sell/item/\d+"[^>]*>(.*?) - (.*?) \(.*?\)<\/a>'
        
        artist_matches = re.findall(artist_name_pattern, xml_file, re.DOTALL)
        
        artist_names = [match[0].strip() for match in artist_matches]
        
        if artist_names:
            print(f'Found {len(artist_names)} artist names')
            return artist_names
        else:
            print('No Matches for artist names')
            return None
            
    def get_record_name(self, file_name):

        xml_file = self.load_xml_file(file_name)
        
        record_name_pattern = r'<td class="item_description">.*?<a href="/sell/item/\d+"[^>]*>(.*?) - (.*?) \(.*?\)<\/a>'
        
        record_matches = re.findall(record_name_pattern, xml_file, re.DOTALL)
        
        record_names = [match[1].strip() for match in record_matches]
        
        if record_names:
            print(f'Found {len(record_names)} artist names')
            return record_names
        else:
            print('No Matches for artist names')
            return None

    def get_media_condition(self, file_name):
        xml_file = self.load_xml_file(file_name)
        
        media_condition_pattern = r'<span>\s*Media Condition:\s*<\/span>\s*<span>(.*?)<\/span>'

        media_condition = re.search(media_condition_pattern, xml_file, re.DOTALL)

        if media_condition:
            media_condition = media_condition.group(1).strip()  # Get the captured group and remove whitespace
            print(f'Found media condition: {media_condition}')
            return media_condition  # Return the media condition
        else:
            print('No Matches for media condition')
            return None 

    def get_sleeve_condition(self, file_name):        
        return None
    
    def get_currency(self, file_name):
        xml_file = self.load_xml_file(file_name)
        currency_pattern = r'[A-Z]{3}'
        currency_match = re.findall(currency_pattern, xml_file)

        if currency_match:
            currency = currency_match[::2] # remove every second entry since it contains desktop + mobile listings
            print(f'Found currency instances: {len(currency)}')
            return currency
        else:
            print('No Matches for currency')
            return None
       
    def get_item_price(self, file_name):
        xml_file = self.load_xml_file(file_name)
        
        item_price_pattern = r'data-pricevalue="(\d+\.\d+)"'
        item_price_matches = re.findall(item_price_pattern, xml_file) 
        if item_price_matches:
            item_price = item_price_matches[::2] # remove every second entry since it contains desktop + mobile listings
            print(f'Found item_price instances: {len(item_price)}')
            return item_price
        else:
            print('No Matches found for Item Price')
            return None
    
    
    def get_seller_name(self, file_name):        
        return None

    def get_seller_rating(self, file_name):        
        return None
    
    def get_shipping_origin(self, file_name):        
        return None
    
    def get_shippin_rate(self, file_name):        
        return None
    
    def get_current_date(self, file_name):        
        return None
        






test = xmlParser()
test.get_listing_id("409250.xml")
test.get_release_id("409250.xml")
test.get_record_name("409250.xml")
test.get_item_price("409250.xml")
test.get_media_condition("409250.xml")
test.get_currency("409250.xml")