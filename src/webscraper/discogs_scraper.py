import time
import random
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from lxml import etree, html

from src.logger import get_logger

logger = get_logger()


class DiscogsScraper:
    def __init__(self):

        options = Options()
        # options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)

    def get_by_release_id(self, wantlist):
        try:

           for release in wantlist:
                release_id = release['release_id']
                title = release['title']

                logger.debug(f"Attempting to scrape '{title}'")
                delay = random.uniform(3, 8)
                time.sleep(delay)

                self.driver.get(
                    f'https://www.discogs.com/sell/release/{release_id}?ev=rb&limit=250')

                discogs_html_content = self.driver.page_source
                discogs_doc = html.fromstring(discogs_html_content)
                discogs_content = discogs_doc.xpath(
                    "//*[@id='pjax_container']/table")

                output_directory_path = os.path.join('src', 'data', 'marketplace_listings')
                output_file_path = os.path.join(output_directory_path, f'{release_id}.xml')

                if not os.path.exists(output_directory_path):
                    os.makedirs(output_directory_path)

                with open(output_file_path, 'wb') as out:
                    out.write(etree.tostring(
                        discogs_content[0], pretty_print=True, encoding='utf-8'))

                logger.info(f"Successfully scraped '{title}'")

        except WebDriverException as e:
            logger.error(f'Error occurred: {e}')
            raise

    def delete_cookies(self):
        self.driver.delete_all_cookies()

    def quit(self):
        self.driver.quit()
