import os

import discogs_client

from src.logger import get_logger

logger = get_logger()

class DiscogsWantlistClient:
    def __init__(self):
        '''
        Initializes the Discogs API client.
        '''
        try:
            user_token = os.getenv('DISCOGS_USER_TOKEN')
            if not user_token:
                raise ValueError(
                    'Discogs user token not found in environment variables.')

            self.client = discogs_client.Client(
                'discoring/1.0', user_token=user_token)
            logger.info('Discogs client initialized successfully.')

        except Exception as e:
            logger.error(f'Error during Discogs authorization process: {e}')

    def get_wantlist(self):

        username = os.getenv('DISCOGS_USERNAME')
        user = self.client.user(username)
        wantlist = user.wantlist
        # don't create  a dictionary for each record (with increasing numbers of entries in a wantlist this will gonna take a while, do it based ont he filter_config)
        wantlist_dict = {record.release.id: {'title': record.release.title,
                                             'genre': record.release.genres,
                                             'artist': [artist.name for artist in record.release.artists],
                                             'label': [label.name for label in record.release.labels],
                                             'year': record.release.year,
                                             'format': record.release.formats,
                                             'country': record.release.country}
                         for record in wantlist}

        return wantlist_dict
