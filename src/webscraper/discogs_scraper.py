from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from lxml import etree,html
import time
import os

load_dotenv()

class DiscogsScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    
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
            
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body"))) # Wait for the page to load and the desired element to be visible
            
            html_content = self.driver.page_source
            
            htmldoc = html.fromstring(html_content)
            
            with open("src\\data\\raw\\wantlister.xml", 'wb') as out: 
                out.write(etree.tostring(htmldoc, pretty_print=True, encoding='utf-8', xml_declaration=True))
                
            print("Successfully generated XML-file from Discogs 'Wantlister' page")
        
        except WebDriverException as e:
            print(f"Error occurred: {e}")
    
    def get_by_release_id(self): # does not require login method
        try:
            self.driver.get(f"https://www.discogs.com/sell/release/31612672?ev=rb")
            
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body"))) # Wait for the page to load and the desired element to be visible
            
            html_content = self.driver.page_source
            
            htmldoc = html.fromstring(html_content)
            
            with open(f"src\\data\\raw\\31612672.xml", 'wb') as out: 
                out.write(etree.tostring(htmldoc, pretty_print=True, encoding='utf-8', xml_declaration=True))
            
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

