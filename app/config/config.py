from asyncio.log import logger
from dotenv import load_dotenv
from pathlib import Path
import os

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    HASHIDS_MIN_LENGTH = os.environ.get('HASHIDS_MIN_LENGTH')
    HASHIDS_ALPHABET = os.environ.get('HASHIDS_ALPHABET')
    HASHIDS_SALT = os.environ.get('HASHIDS_SALT')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
    
class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
        
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

def factory(app: str) -> Config:
    configuration = {
        'testing': TestConfig,
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }
    
    return configuration[app] 
  