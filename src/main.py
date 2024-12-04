from src.scripts.convert_currency import convert_price_to_chf
from src.scripts.convert_discogs_xml import convert_discogs_html_to_xml
from src.scripts.convert_xml_to_dict import convert_wantlist_xml_to_dict
from src.scripts.delete_documents import delete_orphaned_documents
from src.scripts.update_documents import update_listings_in_mongodb

from dotenv import load_dotenv


load_dotenv(override=True)

if __name__ == "__main__":

    convert_discogs_html_to_xml()
    convert_wantlist_xml_to_dict()
    convert_price_to_chf()
    update_listings_in_mongodb()
    delete_orphaned_documents()
