import requests
import discogs_client
from discogs_client import Client, Condition, Status, Sort
from dotenv import load_dotenv
import os

load_dotenv()

user_token = os.getenv('USER_TOKEN')

# Give API credentials to client
client = discogs_client.Client('discoring/1.0', user_token=user_token)

username = 'Behoever'

# Create Record as a class

class Record:
    def __init__(self, artist, title, label):
        self.artist=self
        self.title=title
        self.label=label
        
    @classmethod
    def initialize_client(app, user_token):
        client = discogs_client.Client('discoring/1.0', user_token=user_token)
        


import requests

# Replace 'YOUR_ACCESS_TOKEN' with your actual Discogs API token
headers = {
    'Authorization': os.getenv('USER_TOKEN'),
}

def get_release_marketplace_listings(release_id):
    url = f'https://api.discogs.com/releases/{release_id}/listings'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Example usage
release_id = 'r27928278'  # Replace with the actual release ID you want to fetch listings for
listings = get_release_marketplace_listings(release_id)

if listings:
    for listing in listings['listings']:
        seller = listing['seller']['username']
        price = listing['price']['value']
        currency = listing['price']['currency']
        condition = listing['condition']
        print(f"Seller: {seller}, Price: {price} {currency}, Condition: {condition}")
        




