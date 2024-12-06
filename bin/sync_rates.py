import os

import json

from src.forex.fxratesapi import get_currency_exchange_rate

def sync_chf_exchange_rates():

    exchange_rates = get_currency_exchange_rate()

    output_directory = os.path.join(os.getcwd(), 'src','config')
    file_name = 'chf_exchange_rates_config.json'
    json_filepath = os.path.join(output_directory, file_name)

    with open(json_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(exchange_rates, json_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    sync_chf_exchange_rates()
