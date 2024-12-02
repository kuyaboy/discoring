import os
import json


def convert_price_to_chf():

    listings_directory = os.path.join(os.getcwd(), 'src', 'data', 'listings_json')
    listings = os.listdir(listings_directory)

    rates_directory = os.path.join(os.getcwd(), 'src', 'config')
    rates_file = 'chf_exchange_rates.json'
    rates_path = os.path.join(rates_directory, rates_file)

    with open(rates_path, 'r', encoding='utf-8') as rates_file:
        rates = json.load(rates_file)

    for file_name in listings:
        file_path = os.path.join(listings_directory, file_name)

        with open(file_path, 'r', encoding='utf-8') as listing_file:
            listings = json.load(listing_file)

        for item in range(len(listings)-1):
            currency = listings[item]['currency']
            if listings[item]['currency'] in rates['rates']:
                exchange_rate = float(rates['rates'][currency])
                listings[item]['item_price_chf'] = round(float(listings[item]['item_price']) * (1 / exchange_rate), 2)

        with open(file_path, 'w', encoding='utf-8') as listing_file:
            json.dump(listings, listing_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    convert_price_to_chf()

