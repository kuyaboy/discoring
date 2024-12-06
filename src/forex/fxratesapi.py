import os

import requests

from src.logger import logger

def get_currency_exchange_rate():
    url = f"https://api.fxratesapi.com/latest?api_key={os.getenv('FXRATES_API_TOKEN')}&base=CHF&places=2"

    try:
        logger.info(f"Making GET request to {url}")
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for non-2xx status codes
        exchange_rate = response.json()
        logger.info(f"Successfully fetched exchange rate data")

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred during the GET request to {url}: {e}", exc_info=True)
        return None

    return exchange_rate

