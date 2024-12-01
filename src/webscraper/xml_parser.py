import os
import regex as re

from src.helper.filter_duplicate_prices import filter_unique_prices

class xmlParser:
    def __init__(self):
        self.root = None

    def load_xml_file(self, file_name):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, 'src', 'data', 'marketplace_listings', file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_listing_id(self, file_name):
        xml_file = self.load_xml_file(file_name)

        listing_pattern = r'<td class="item_description">.*?<a href="/sell/item/(\d+)"[^>]*>'
        listing_ids = re.findall(listing_pattern, xml_file, re.DOTALL)
        no_entry = []

        if listing_ids:
            print(f'Found {len(listing_ids)} instances for listing ID')
            return listing_ids
        else:
            no_entry.append("NaN")
            return no_entry

    def get_release_id(self, file_name):
        xml_file = self.load_xml_file(file_name)

        release_pattern = r'<a href="/release/(\d+)-[^"]*" class="item_release_link hide_mobile">View Release Page<\/a>'
        release_ids = re.findall(release_pattern, xml_file, re.DOTALL)
        no_entry = []
        

        if release_ids:
            print(f'Found {len(release_ids)} instances for {(release_ids[0])}')
            return release_ids
        else:
            no_entry.append(file_name.split(".")[0])
            return no_entry
            

    def get_artist_name(self, file_name):
        xml_file = self.load_xml_file(file_name)

        artist_name_pattern = r'<td class="item_description">.*?<a href="/sell/item/\d+"[^>]*>(.*?) - (.*?) \(.*?\)<\/a>'
        artist_matches = re.findall(artist_name_pattern, xml_file, re.DOTALL)
        artist_names = [match[0].strip() for match in artist_matches]
        no_entry = []

        if artist_names:
            print(f'Found {len(artist_names)} artist names')
            return artist_names
        else:
            no_entry.append("NaN")
            return no_entry
            

    def get_record_name(self, file_name):
        xml_file = self.load_xml_file(file_name)

        record_name_pattern = r'<td class="item_description">.*?<a href="/sell/item/\d+"[^>]*>(.*?) - (.*?) \(.*?\)<\/a>'
        record_matches = re.findall(record_name_pattern, xml_file, re.DOTALL)
        record_names = [match[1].strip() for match in record_matches]
        no_entry = []
            

        if record_names:
            print(f'Found {len(record_names)} artist names')
            return record_names
        else:
            no_entry.append("NaN")
            return no_entry

    def get_media_condition(self, file_name):
        xml_file = self.load_xml_file(file_name)

        media_condition_pattern = r'<span>\s*([\w\s\(\)+\-]+)\s*<span'
        media_condition_matches = re.findall(media_condition_pattern, xml_file, re.DOTALL)

        media_condition = []
        no_entry = []

        if media_condition_matches:
            for condition in media_condition_matches:
                media_condition.append(condition.strip())

            print(f'Found Media condition instances: {len(media_condition)}')
            return media_condition
        else:
            no_entry.append("NaN")
            return no_entry

    def get_sleeve_condition(self, file_name):
        xml_file = self.load_xml_file(file_name)

        item_pattern = r'<td class="item_description">(.*?)</td>'
        sleeve_condition_pattern = r'<span class="item_sleeve_condition">(.*?)</span>'

        items = re.findall(item_pattern, xml_file, re.DOTALL)
        sleeve_conditions = []

        for item in items:
            match = re.search(sleeve_condition_pattern, item, re.DOTALL)
            if match:
                sleeve_conditions.append(match.group(1).strip())
            else:
                sleeve_conditions.append("NaN")

        return sleeve_conditions if sleeve_conditions else ["NaN"]


    def get_currency(self, file_name):
        xml_file = self.load_xml_file(file_name)

        currency_pattern = r'data-currency="([A-Z]{3})"'
        currency_matches = re.findall(currency_pattern, xml_file)
        no_entry = []
        
        if currency_matches:
            currency = currency_matches[::2]
            print(f'Found currency instances: {len(currency)}')
            return currency
        else:
            no_entry.append("NaN")
            print('No Matches for currency')
            return no_entry

    def get_item_price(self, file_name):
        xml_file = self.load_xml_file(file_name)

        item_price_pattern = r'data-pricevalue="(\d+\.\d+)"'
        item_price_matches = re.findall(item_price_pattern, xml_file)
        no_entry = []

        if item_price_matches:
            item_price = item_price_matches[::2]  # remove every second entry since it contains desktop + mobile listings
            print(f'Found item_price instances: {len(item_price)}')
            return item_price
        else:
            no_entry.append("NaN")
            print('No Matches found for Item Price')
            return no_entry

    def get_seller_name(self, file_name):
        xml_file = self.load_xml_file(file_name)

        seller_name_pattern = r'data-seller-username="(.*?)"'
        seller_name_matches = re.findall(seller_name_pattern, xml_file, re.DOTALL)
        no_entry= []

        if seller_name_matches:
            seller_name = seller_name_matches[::2]  # remove every second entry since it contains desktop + mobile listings
            print(f'Found Seller name instances: {len(seller_name)}')
            return seller_name
        else:
            no_entry.append("NaN")
            print("Walang nahanap")
            return no_entry

    def get_seller_rating(self, file_name):
        xml_file = self.load_xml_file(file_name)

        seller_rating_pattern = r'<strong>([\d\.]+%)<\/strong>'
        seller_rating = re.findall(seller_rating_pattern, xml_file, re.DOTALL)
        no_entry = []

        if seller_rating:
            print(f'Found seller rating instances: {len(seller_rating)}')
            return seller_rating
        else:
            no_entry.append("NaN")
            print("Walang nahanap")
            return no_entry

    def get_shipping_origin(self, file_name):
        xml_file = self.load_xml_file(file_name)

        shipping_origin_pattern = r'<span class="mplabel">Ships From:</span>(.*?)<\/li>'
        shipping_origin = re.findall(shipping_origin_pattern, xml_file)
        no_entry = []
        
        if shipping_origin:
            print(f'Shipping Origin instances found: {len(shipping_origin)}')
            return shipping_origin
        else:
            no_entry.append("NaN")
            print('No shipping origin found')
            return no_entry

    def get_shipping_price(self, file_name):
        xml_file = self.load_xml_file(file_name)

        # Define combined regex pattern for shipping prices and unavailable messages
        combined_shipping_price_pattern = (
            r'<span class="hide_mobile item_shipping">\s*[+][A-Z]{3}(\d+\.\d+)'  # cases like +CHF / match[0]
            r'|<span class="hide_mobile item_shipping">\s*[+][A-Z]{2}\p{Sc}(\d+\.\d+)'  # cases like +CA$40.00 / match[1]
            r'|<span class="hide_mobile item_shipping">\s*[+][A-Z]{1}\p{Sc}(\d+\.\d+)' # cases like +A$50.00
            r'|<span class="hide_mobile item_shipping">\s*[+]\p{Sc}(\d+\.\d+)'  # cases like +$ / match[2]
            r'|<span class="hide_mobile item_shipping">\s*[+]\p{Sc}(\d+\,\d+)'  # cases like +¥1,690 / match [2]
            r'|<p class="hide-desktop muted">\s*(Unavailable in .*?)\s*</p>' # cases like Unavailable in Philippines / match[3]'
        )

        combined_shipping_price_match = re.finditer(combined_shipping_price_pattern, xml_file)
        shipping_prices_all = []  # this list still contains duplicates
        no_entry = []

        for match in combined_shipping_price_match:
            for group in match.groups():
                if group:
                   shipping_prices_all.append(group.strip())
                        
        if shipping_prices_all:
            shipping_prices = filter_unique_prices(shipping_prices_all)
            print(f'Shipping prices instances without duplicates: {len(shipping_prices)}')
            return shipping_prices
        else:
            no_entry.append("NaN")
            print("No prices found")
            return no_entry