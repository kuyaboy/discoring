import os

import requests

from dotenv import load_dotenv

load_dotenv(override=True)

def get_currency_exchange_rate():

    url = f"https://api.fxratesapi.com/latest?api_key={os.getenv('FXRATES_API_TOKEN')}&base=CHF&places=2"

    response = requests.get(url)
    exchange_rate = response.json()

    return exchange_rate
