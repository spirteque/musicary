from datetime import datetime
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

def spotify_headers_manager():
    # https://stackoverflow.com/questions/1291755/how-can-i-tell-whether-my-django-application-is-running-on-development-server-or
    if settings.DEBUG:
        logger.info(msg='Using Spotify headers manager DEBUG version.')
        
        def create():
            return {
                'Authorization': f'Bearer {settings.DEBUG_SPOTIFY_TOKEN}'
            }
            
        return create
    
    previous_time = None
    headers = None
    
    def create():
        nonlocal previous_time
        nonlocal headers
        
        current_time = datetime.now()
        if previous_time:
            should_fetch_new_token = getattr(current_time - previous_time, 'seconds', 0) >= 3000
        else:
            should_fetch_new_token = True
            
        if not should_fetch_new_token:
            logger.info(msg='Present token is up to date, using: ' + headers['Authorization'][0:15] + '... .')
        
        if not headers or should_fetch_new_token:
            spotify_access_response = requests.post(url=settings.SPOTIFY_API_TOKEN_URL,
                                                    data={
                                                        'grant_type': 'client_credentials',
                                                        'client_id': settings.SPOTIFY_CLIENT_ID,
                                                        'client_secret': settings.SPOTIFY_CLIENT_SECRET
                                                    })
            
            json = spotify_access_response.json()
            previous_time = current_time
            token_type = json['token_type']
            access_token = json['access_token']
            headers = {'Authorization': f'{token_type} {access_token}'}
            
            logger.info(msg='Token has been updated, using: ' + headers['Authorization'][0:15] + '... .')
            
        return headers
    
    return create

create_spotify_headers = spotify_headers_manager()
