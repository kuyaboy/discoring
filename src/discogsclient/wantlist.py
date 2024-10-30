import os

import discogs_client

from dotenv import load_dotenv

load_dotenv(override=True)

class DiscogsWantlistClient:
    def __init__(self):
        '''
        Initializes the Discogs API client.
        '''
        try:
            user_token = os.getenv('DISCOGS_USER_TOKEN')
            if not user_token:
                raise ValueError('Discogs user token not found in environment variables.')

            # Initialize the Discogs client
            self.client = discogs_client.Client('discoring/1.0', user_token=user_token)
            print('Discogs client initialized successfully.')

        except Exception as e:
            print(f'Error during Discogs authorization process: {e}')
        
    def get_wantlist(self):
        
        username = os.getenv('DISCOGS_USERNAME')
        
        user = self.client.user(username)
        
        wantlist = user.wantlist
        
        wantlist_dict = {item.release.id: {'title': item.release.title, 
                                              'artist': [artist.name for artist in item.release.artists], 
                                              'label': [label.name for label in item.release.labels], 
                                              'year': item.release.year} 
                         for item in wantlist}
        
        return wantlist_dict
