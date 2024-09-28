from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from lxml import etree,html
import time
import os

load_dotenv()

class DiscogsScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    def login(self):
        try:
            self.driver.get("https://www.discogs.com/login")
            
            element_username = self.driver.find_element(By.ID,"username")
            element_password = self.driver.find_element(By.NAME,"password")
            
            element_username.send_keys(os.getenv('DISCOGS_USERNAME'))
            element_password.send_keys(os.getenv('DISCOGS_PASSWORD'))
            
            continue_button = self.driver.find_element(By.CLASS_NAME, "ca0df71c7")
            continue_button.click()
            
            print(f"Successfully login into Discogs as user: {os.getenv('DISCOGS_USERNAME')}")
        
        except WebDriverException as e:
            print(f"Error occurred: {e}")
            
    def get_wantlister_xml(self): # requires login method
        try:
            self.driver.get("https://wantlister.discogs.com")
            
            accept_cookies_button = self.driver.find_elements(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            
            if accept_cookies_button:
                WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
                ).click()
            
            else:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body"))) # Wait for the page to load and the desired element to be visible
                    
                parser = etree.HTMLParser()
                    
                html_page = self.driver.page_source
                    
                html_root = etree.fromstring(html_page, parser)
                    
                html_xml_parsed = etree.tostring(html_root, pretty_print = True, method = "html")
                    
                with open("src\\data\\raw\\wantlister.xml", 'wb') as out: 
                    out.write(html_xml_parsed)
                        
                print("Successfully generated XML-file from Discogs 'Wantlister' page")
        
        except WebDriverException as e:
            print(f"Error occurred: {e}")
    
    def get_by_release_id(self): # does not require login method
        
        try:
            
            self.driver.implicitly_wait(3)

            self.driver.get(f"https://www.discogs.com/sell/release/31612672?ev=rb")
            
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]'))).click() # Wait for the page to load and the desired element to be visible
            
            
            discogs_html_content = self.driver.page_source
            
            
            discogs_doc = html.fromstring(discogs_html_content)
            
            
            discogs_content = discogs_doc.xpath('//*[@id="pjax_container"]')
            
            if len(discogs_content) == 0:
               print("Something went wrong: XML file is empty")
                
            else:
                
                with open(f"src\\data\\raw\\31612672.xml", 'wb') as out: 
                    out.write(etree.tostring(discogs_content[0], pretty_print=True, encoding='utf-8', xml_declaration=True))
                    
                print("Successfully scraped marketplace of release with id: ")
            
        except WebDriverException as e:
            print(f"Error occurred: {e}")
                
    def delete_cookies(self):
        self.driver.delete_all_cookies()
    
    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    scraper = DiscogsScraper()
    scraper.login()
    scraper.get_wantlister_xml()
    scraper.get_by_release_id()
    scraper.delete_cookies()
    scraper.quit()
