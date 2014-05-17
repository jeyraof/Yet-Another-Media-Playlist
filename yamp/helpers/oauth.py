# -*- coding: utf-8 -*-

from flask import session
from flask_oauth import OAuth
from yamp.app import app

config = app.config
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.googleapis.com/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=config.get('GOOGLE_CLIENT_ID'),
                          consumer_secret=config.get('GOOGLE_CLIENT_SECRET'))
GOOGLE_TOKEN_NAME = 'google_access_token'

@google.tokengetter
def get_google_access_token():
    return session.get(GOOGLE_TOKEN_NAME)


class GoogleAPI(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def fetch(self):
        param = {
            'access_token': self.access_token,
            'alt': 'json',
        }
        r = google.get('/oauth2/v2/userinfo', data=param)
        return r