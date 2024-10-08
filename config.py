import os

from dotenv import load_dotenv
load_dotenv()

class Config(object):
    API_KEY = os.getenv('API_KEY')
    YOUTUBE_VIDEO_ID = os.getenv('YOUTUBE_VIDEO_ID')
    DEBUG = os.getenv("DEBUG") or False