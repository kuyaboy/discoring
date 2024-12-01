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
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def login(self):
        try:
            self.driver.get('https://www.discogs.com/login')

            element_username = self.driver.find_element(By.ID, 'username')
            element_password = self.driver.find_element(By.NAME, 'password')

            element_username.send_keys(os.getenv('DISCOGS_USERNAME'))
            element_password.send_keys(os.getenv('DISCOGS_PASSWORD'))

            continue_button = self.driver.find_element(By.CLASS_NAME, 'ca0df71c7')
            continue_button.click()

            print(f"Successfully logged in to Discogs as user: {os.getenv('DISCOGS_USERNAME')}")

        except WebDriverException as e:
            print(f'Error occurred during login: {e}')

    def get_by_release_id(self, wantlist):
        try:

            for release in wantlist:
                release_id = release['release_id']
                title = release['title']

                delay = random.uniform(3, 8)
                time.sleep(delay)

                self.driver.get(f'https://www.discogs.com/sell/release/{release_id}?ev=rb&limit=250')

                # accept_cookies_button = self.driver.find_elements(By.XPATH, "//*[@id='onetrust-accept-btn-handler']")

                # if accept_cookies_button:
                #     print("found cookie button")
                #     time.sleep(2)

                #     WebDriverWait(self.driver, 5).until(
                #         EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))
                #     ).click()
                # else:
                #     WebDriverWait(self.driver, 10).until(
                #         EC.visibility_of_element_located((By.ID, 'pjax_container')))
                discogs_html_content = self.driver.page_source
                discogs_doc = html.fromstring(discogs_html_content)
                discogs_content = discogs_doc.xpath("//*[@id='pjax_container']/table")

                if not discogs_content:
                    print('Something went wrong: XML file is empty')
                else:
                    with open(f'src\\data\\marketplace_listings\\{release_id}.xml', 'wb') as out:
                        out.write(etree.tostring(discogs_content[0], pretty_print=True, encoding='utf-8'))

                    print(f'Successfully scraped marketplace for {title}')

        except WebDriverException as e:
            print(f'Error occurred: {e}')

    def delete_cookies(self):
        self.driver.delete_all_cookies()

    def quit(self):
        self.driver.quit()
