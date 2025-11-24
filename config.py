import os
from dotenv import load_dotenv

load_dotenv()

DEV = 'development'
PROD = 'production'
DEFAULT = 'default'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    DEV: DevelopmentConfig,
    PROD: ProductionConfig,
    DEFAULT: DevelopmentConfig
}
