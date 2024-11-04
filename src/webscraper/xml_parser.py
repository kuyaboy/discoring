import os
import regex as re

from src.helper.filter_duplicate_prices import filter_unique_prices

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
            return []

    def get_release_id(self, file_name):
        xml_file = self.load_xml_file(file_name)

        release_pattern = r'<a href="/release/(\d+)-[^"]*" class="item_release_link hide_mobile">View Release Page<\/a>'
        release_ids = re.findall(release_pattern, xml_file, re.DOTALL)

        if release_ids:
            print(f'Found {len(release_ids)} instances for release ID')
            return release_ids
        else:
            print('No Matches for release_id')
            return []

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
            return []

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
            return []

    def get_media_condition(self, file_name):
        # Load the XML file content
        xml_file = self.load_xml_file(file_name)

        media_condition_pattern = r'<span>\s*([\w\s\(\)+\-]+)\s*<span'
        media_condition_matches = re.findall(media_condition_pattern, xml_file, re.DOTALL)

        media_condition = []

        if media_condition_matches:
            for condition in media_condition_matches:
                media_condition.append(condition.strip())

            print(f'Found Media condition instances: {len(media_condition)}')
            return media_condition
        else:
            print("Media Condition not found.")
            return []

    def get_sleeve_condition(self, file_name):
        xml_file = self.load_xml_file(file_name)

        sleeve_condition_pattern = r'<span class="item_sleeve_condition">(.*?)<\/span>'
        sleeve_condition = re.findall(sleeve_condition_pattern, xml_file, re.DOTALL)

        if sleeve_condition:
            print(f'Found Sleeve condition instances: {len(sleeve_condition)}')
            return sleeve_condition
        else:
            print("Walang nahanap")
            return []

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
            return []

    def get_item_price(self, file_name):
        xml_file = self.load_xml_file(file_name)

        item_price_pattern = r'data-pricevalue="(\d+\.\d+)"'
        item_price_matches = re.findall(item_price_pattern, xml_file)

        if item_price_matches:
            item_price = item_price_matches[::2]  # remove every second entry since it contains desktop + mobile listings
            print(f'Found item_price instances: {len(item_price)}')
            return item_price
        else:
            print('No Matches found for Item Price')
            return []

    def get_seller_name(self, file_name):
        xml_file = self.load_xml_file(file_name)

        seller_name_pattern = r'data-seller-username="(.*?)"'
        seller_name_matches = re.findall(seller_name_pattern, xml_file, re.DOTALL)

        if seller_name_matches:
            seller_name = seller_name_matches[::2]  # remove every second entry since it contains desktop + mobile listings
            print(f'Found Seller name instances: {len(seller_name)}')
            return seller_name
        else:
            print("Walang nahanap")
            return []

    def get_seller_rating(self, file_name):
        xml_file = self.load_xml_file(file_name)

        seller_rating_pattern = r'<strong>([\d\.]+%)<\/strong>'
        seller_rating = re.findall(seller_rating_pattern, xml_file, re.DOTALL)

        if seller_rating:
            print(f'Found seller rating instances: {len(seller_rating)}')
            return seller_rating
        else:
            print("Walang nahanap")
            return []

    def get_shipping_origin(self, file_name):
        xml_file = self.load_xml_file(file_name)

        shipping_origin_pattern = r'<span class="mplabel">Ships From:</span>(.*?)<\/li>'
        shipping_origin = re.findall(shipping_origin_pattern, xml_file)

        if shipping_origin:
            print(f'Shipping Origin instances found: {len(shipping_origin)}')
            return shipping_origin
        else:
            print('No shipping origin found')
            return []

    def get_shipping_price(self, file_name):
        xml_file = self.load_xml_file(file_name)

        # Define combined regex pattern for shipping prices and unavailable messages
        combined_shipping_price_pattern = (
            r'<span class="hide_mobile item_shipping">\s*[+][A-Z]{3}(\d+\.\d+)'  # cases like +CHF / match[0]
            r'|<span class="hide_mobile item_shipping">\s*[+][A-Z]{2}\p{Sc}(\d+\.\d+)'  # cases like +CA$40.00 / match[1]
            r'|<span class="hide_mobile item_shipping">\s*[+]\p{Sc}(\d+\.\d+)'  # cases like +$ / match[2]
            r'|<p class="hide-desktop muted">\s*(Unavailable in .*?)\s*</p>'  # cases like Unavailable in Philippines / match[3]
        )

        combined_shipping_price_match = re.findall(combined_shipping_price_pattern, xml_file)
        shipping_prices_all = []  # this list still contains duplicates

        for match in combined_shipping_price_match:
            if match[0]:  # Shipping prices
                shipping_prices_all.append(f'{match[0]}')
            elif match[1]:
                shipping_prices_all.append(f'{match[1]}')
            elif match[2]:
                shipping_prices_all.append(f'{match[2]}')
            elif match[3]:  # Unavailable message
                shipping_prices_all.append(match[3])

        print(shipping_prices_all)

        if shipping_prices_all:
            shipping_prices = filter_unique_prices(shipping_prices_all)
            print(f'Shipping prices instances: {len(shipping_prices)}')
            return shipping_prices
        else:
            return []
