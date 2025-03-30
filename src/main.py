#!/opt/venv/bin/python3
import time

from dotenv import load_dotenv
load_dotenv()

from logger import get_logger
from scripts.convert_currency import convert_price_to_chf
from scripts.convert_discogs_xml import convert_discogs_html_to_xml
from scripts.convert_xml_to_dict import convert_wantlist_xml_to_dict
from scripts.delete_documents import delete_orphaned_documents
from scripts.update_documents import update_listings_in_mongodb
from telegram.discoring_notifier import check_and_notify

if __name__ == "__main__":
    logger = get_logger()

    try:
        logger.info('Starting the scraping cycle.')

        start_time = time.time()

        logger.debug('Converting scraped Discogs HTML to XML.')
        convert_discogs_html_to_xml()
        logger.info('Successfully converted Discogs HTML to XML.')

        logger.debug('Converting wantlist XML to dictionary.')
        convert_wantlist_xml_to_dict()
        logger.info('Successfully converted wantlist XML to dictionary.')

        logger.debug('Converting prices to CHF.')
        convert_price_to_chf()
        logger.info('Successfully converted prices to CHF.')

        logger.debug('Updating listings in MongoDB.')
        update_listings_in_mongodb()
        logger.info('Successfully updated listings in MongoDB.')

        logger.debug('Deleting orphaned documents.')
        delete_orphaned_documents()

        logger.debug('Querying MongoDB for good sales.')
        check_and_notify()
        logger.info('Successfully notified in the event of a good sale.')

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f'Scraping cycle completed in {execution_time:.2f} seconds.')

    except Exception as e:
        logger.error(f'An error occurred during the scraping process: {str(e)}', exc_info=True)
