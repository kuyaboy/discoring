from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()

options = Options()
options.add_argument("--headless") 
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def discogs_login():
    try:
        # Attempt to load the website in headless mode
        driver.get("https://www.discogs.com/login?prompt=login&amp;return_to=https%3A%2F%2Fwww.discogs.com%2F")
         
        # Insert login-credentials
        
        element_username = driver.find_element(By.ID, "username")
        element_password = driver.find_element(By.NAME, "password")
        
        element_username.send_keys(os.getenv('DISCOGS_USERNAME'))
        element_password.send_keys(os.getenv('DISCOGS_PASSWORD'))
        
        continue_button = driver.find_element(By.CLASS_NAME, "ca0df71c7")
        continue_button.click()
        
        print(f"Successfully login into Discogs as user: {os.getenv('DISCOGS_USERNAME')}")
        
    except WebDriverException as e:
        # Handle the exception and print the error code/message
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    discogs_login()

