from src.scripts.convert_discogs_xml import convert_discogs_html_to_xml
from src.scripts.convert_xml_to_dict import convert_wantlist_xml_to_dict
from src.scripts.import_to_mongodb import import_listings_to_mongodb


def main():

    convert_discogs_html_to_xml()
    convert_wantlist_xml_to_dict()
    import_listings_to_mongodb()


if __name__ == "__main__":
    main()
