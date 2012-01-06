import os

class Config(object):
    DEBUG = True
    TESTING = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
    FB_APP_SCOPE = []
    FB_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    FB_APP_SECRET = os.environ.get('FACEBOOK_SECRET')
