import os
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from lxml import etree, html

load_dotenv()


class DiscogsScraper:
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)

    def get_by_release_id(self, wantlist):
        try:

            for release in wantlist:
                release_id = release['release_id']
                title = release['title']

                delay = random.uniform(3, 8)
                time.sleep(delay)

                self.driver.get(
                    f'https://www.discogs.com/sell/release/{release_id}?ev=rb&limit=250')

                discogs_html_content = self.driver.page_source
                discogs_doc = html.fromstring(discogs_html_content)
                discogs_content = discogs_doc.xpath(
                    "//*[@id='pjax_container']/table")

                if not discogs_content:
                    print('Something went wrong: XML file is empty')
                else:
                    with open(f'src\\data\\marketplace_listings\\{release_id}.xml', 'wb') as out:
                        out.write(etree.tostring(
                            discogs_content[0], pretty_print=True, encoding='utf-8'))

                    print(f'Successfully scraped marketplace for {title}')

        except WebDriverException as e:
            print(f'Error occurred: {e}')

    def delete_cookies(self):
        self.driver.delete_all_cookies()

    def quit(self):
        self.driver.quit()
