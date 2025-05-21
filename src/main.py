#!/opt/venv/bin/python3
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()

from logger import get_logger
from scripts.convert_currency import convert_price_to_currency
from scripts.convert_discogs_xml import convert_discogs_html_to_xml
from scripts.convert_xml_to_dict import convert_wantlist_xml_to_dict
from scripts.delete_documents import delete_orphaned_documents
from scripts.update_documents import update_listings_in_mongodb
from telegram.notifier import check_and_notify

logger = get_logger()

def run_cycle():
    logger.info('Starting the scraping cycle.')
    start_time = time.time()

    currency_upper = os.getenv('CURRENCY').upper()

    logger.debug('Converting scraped Discogs HTML to XML.')
    convert_discogs_html_to_xml()
    logger.info('Successfully converted Discogs HTML to XML.')

    logger.debug('Converting wantlist XML to dictionary.')
    convert_wantlist_xml_to_dict()
    logger.info('Successfully converted wantlist XML to dictionary.')

    logger.debug(f'Converting item prices to {currency_upper}.')
    convert_price_to_currency()
    logger.info(f'Successfully converted prices to {currency_upper}.')

    logger.debug('Updating listings in MongoDB.')
    update_listings_in_mongodb()

    logger.debug('Deleting orphaned documents.')
    delete_orphaned_documents()

    logger.debug('Querying MongoDB for good sales.')
    check_and_notify()
    logger.info('Successfully notified in the event of a good sale.')

    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f'Scraping cycle completed in {execution_time:.2f} seconds.')

if __name__ == "__main__":
    try:
        while True:
            run_cycle()

            # Wait between 4 to 8 minutes before running again
            wait_time = random.randint(240, 480)
            logger.info(f'Waiting {wait_time} seconds before the next cycle...')
            time.sleep(wait_time)

    except Exception as e:
        logger.error(f'Fatal error: {str(e)}', exc_info=True)
