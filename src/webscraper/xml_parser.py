import os
import regex as re

"""
What do I need?:

- listing id --> <td class="item_description">
                <strong>
        <a href="/sell/item/3257360867" class="item_description_title" data-followable="true">Ikee - Sky`s Da Limit / Rock On (12", RE)</a>

- ReleaseID --> "@id": "https://www.discogs.com/release/31612672-Ikee-Skys-Da-Limit-Rock-On"

- Name --> "releaseOf": {
  "@type": "MusicAlbum",
  "name": "Sky`s Da Limit / Rock On",

- Media Condition --> <p class="item_condition">
        <span class="mplabel condition-label-desktop">
            Media Condition:
        </span>
        <span class="mplabel condition-label-mobile">Media:</span>
                
    <span>
        Mint (M)

                    <span class="has-tooltip" role="note" tabindex="0">
                <i class="icon icon-info-circle muted" role="img" aria-hidden="true"/>
                <span class="tooltip multi-line-tooltip sr-only" role="tooltip">
                    <span class="tooltip-inner">
                                                Absolutely perfect in every way. Certainly never been played. Should be used sparingly as a grade.            
                    </span>
                </span>
            </span>
            </span>

- Sleeve Condition --> <span class="item_sleeve_condition">Mint (M)</span>

- Seller name --> data-seller-username="bruceforsight"

- Seller Rating --> <span class="star_rating" alt="bruceforsight rating 5.0 stars out of 5" role="img" aria-label="bruceforsight rating 5.0 out of 5"><i role="img" aria-hidden="true" class="icon icon-star"/><i role="img" aria-hidden="true" class="icon icon-star"/><i role="img" aria-hidden="true" class="icon icon-star"/><i role="img" aria-hidden="true" class="icon icon-star"/><i role="img" aria-hidden="true" class="icon icon-star"/></span> 
    <strong>100.0%</strong><span>,</span>    <a href="/sell/seller_feedback/bruceforsight" target="_top" class="section_link">
        1,051 ratings    </a>
            </li>

- Ships From --> <li><span class="mplabel">Ships From:</span>United Kingdom</li>

- Item Price --> <span class="price" data-currency="GBP" data-pricevalue="23.99">£23.99</span>

- Shipping Price 
        <span class="hide_mobile item_shipping">
        +£7.50
                <i class="icon icon-truck" role="img"/>
                <button class="show-shipping-methods hide_mobile" data-seller-username="bruceforsight" data-seller-id="238461">shipping</button>

- added to database
- check if still available (otherwise delete)

"""
class xmlParser:
    def __init__(self):
            self.root = None

    def load_xml_file(self, file_name):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, 'src', 'data', 'raw', file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()  # Return the content of the file
    
    def get_listing_id(self, file_name):
        xml_file = self.load_xml_file(file_name)
        
        listing_id = re.findall(r"/sell/item/(\d+)", xml_file)
        
        if listing_id != None:
            print(f"Found {len(listing_id)} instances for listing id")
            return listing_id # Return the matched string
        else:
            print("No Matches for listing_id")
            return None
    
    def get_release_id(self, file_name):
        xml_file = self.load_xml_file(file_name)
        
        release_id = re.findall(r"/release/(\d+)[-\w]+", xml_file)
        
        if release_id != None:
            print(f"Found {len(release_id)} instances for release id")
            return release_id  # Return the matched string
        else:
            print("No Matches for release_id")
            return None
    
    def get_item_price(self, file_name):
        xml_file = self.load_xml_file(file_name)
        
        release_id = re.findall(r"span class="price" data-currency=[A-Z]{3} data-pricevalue=(\d+)>£23.99</span>(\d+)[-\w]+", xml_file)
        
        if release_id != None:
            print(f"Found {len(release_id)} instances for release id")
            return release_id  # Return the matched string
        else:
            print("No Matches for release_id")
            return None
        






test = xmlParser()

xml = test.load_xml_file("31612672.xml")
print(xml)

test.get_listing_id("31612672.xml")
test.get_release_id("31612672.xml")