import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    # ........................... Database .........................................
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    # ........................... App Configs .......................................
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST')
    FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT')
    # ............................. API ..............................................
    API_TITLE = os.getenv('API_TITLE')
    API_VERSION = os.getenv('API_VERSION')
    OPENAPI_VERSION = os.getenv('OPENAPI_VERSION')
    OPENAPI_URL_PREFIX = os.getenv('OPENAPI_URL_PREFIX')
    OPENAPI_SWAGGER_UI_PATH = os.getenv('OPENAPI_SWAGGER_UI_PATH')
    OPENAPI_SWAGGER_UI_URL= os.getenv('OPENAPI_SWAGGER_UI_URL')
    JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')
    # ......................... JWT ....................................................
    # JWT_ACCESS_TOKEN_EXPIRES= os.getenv('JWT_ACCESS_TOKEN_EXPIRES')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)



class Developement(Config):
    DEBUG = True

class Production(Config):
    DEBUG = False
