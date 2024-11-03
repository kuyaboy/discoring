import os
import regex as re

class xmlParser:
    def __init__(self):
            self.root = None

    def load_xml_file(self, file_name):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, 'src', 'data', 'raw', file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def get_listing_id(self, file_name):
        xml_file = self.load_xml_file(file_name)
        
        listing_pattern = r'<td class="item_description">.*?<a href="/sell/item/(\d+)"[^>]*>'
        listing_ids = re.findall(listing_pattern, xml_file, re.DOTALL)
        
        if listing_ids:
            print(f'Found {len(listing_ids)} instances for listing ID')
            return listing_ids
        else:
            print('No Matches for release_id')
            return None
        
    def get_release_id(self, file_name):
        xml_file = self.load_xml_file(file_name)

        release_pattern = r'<a href="/release/(\d+)-[^"]*" class="item_release_link hide_mobile">View Release Page<\/a>'
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
        # Load the XML file content
        xml_file = self.load_xml_file(file_name)
        
        media_condition_pattern = r'<span>\s*([\w\s\(\)+\-]+)\s*<span'
        media_condition_matches = re.findall(media_condition_pattern, xml_file, re.DOTALL)
        
        media_condition = []

        if media_condition_matches:
            for condition in media_condition_matches:
                media_condition.append(condition.strip())
        
            print(media_condition)
        else:
            print("Media Condition not found.")

    def get_sleeve_condition(self, file_name):   
        
        xml_file = self.load_xml_file(file_name)
        
        sleeve_condition_pattern = r'<span class="item_sleeve_condition">(.*?)<\/span>'
        sleeve_condition = re.findall(sleeve_condition_pattern, xml_file, re.DOTALL)
        
        if sleeve_condition:
            print(f'Found Sleeve condition instances: {len(sleeve_condition)}')
            return sleeve_condition
        else:
            print("Walang nahanap")
            return None
        
    def get_currency(self, file_name):
        xml_file = self.load_xml_file(file_name)
        
        currency_pattern = r'data-currency="([A-Z]{3})"'
        currency_matches = re.findall(currency_pattern, xml_file)

        if currency_matches:
            currency = currency_matches[::2]
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
        
        xml_file = self.load_xml_file(file_name)
        
        seller_name_pattern = r'data-seller-username="(.*?)"'
        seller_name_matches = re.findall(seller_name_pattern, xml_file, re.DOTALL)
        
        if seller_name_matches:
            seller_name = seller_name_matches[::2] # remove every second entry since it contains desktop + mobile listings
            print(f'Found Seller name instances: {len(seller_name)}')
            return seller_name
        else:
            print("Walang nahanap")
            return None

    def get_seller_rating(self, file_name):
        
        xml_file = self.load_xml_file(file_name)
        
        seller_rating_pattern = r'<strong>([\d\.]+%)<\/strong>'
        seller_rating = re.findall(seller_rating_pattern, xml_file, re.DOTALL)
        
        if seller_rating:
            print(f'Found seller rating instances: {seller_rating}')
        else:
            print("Walang nahanap")
            return None
    
    def get_shipping_origin(self, file_name):
        
        xml_file = self.load_xml_file(file_name)
        
        shipping_origin_pattern = r'<span class="mplabel">Ships From:</span>(.*?)<\/li>'
        shipping_origin = re.findall(shipping_origin_pattern, xml_file)
        
        if shipping_origin:
            print(f'Shipping Origin instances found: {len(shipping_origin)}')
            return shipping_origin
        else:
            print("No shipping origin found")
            return None
        
    def get_shipping_price(self, xml_content):
        # Define regex patterns for shipping prices and availability messages
        shipping_pattern = r'<span class="hide_mobile item_shipping">\s*\+(\$[0-9,]+\.[0-9]{2})\s*</span>'
        unavailable_pattern = r'<p class="hide-desktop muted">\s*Unavailable in [\w\s]+\s*</p>'

        # List to hold shipping prices or messages
        shipping_prices = []

        # Find all shipping prices using regex
        shipping_matches = re.findall(shipping_pattern, xml_content)
        shipping_prices.extend(shipping_matches)

        # Find all unavailable messages using regex
        unavailable_matches = re.findall(unavailable_pattern, xml_content)
        for _ in unavailable_matches:
            shipping_prices.append("Unavailable in your country")

        return shipping_prices
        






test = xmlParser()
test.get_media_condition("225817.xml")
test.get_release_id("225817.xml")