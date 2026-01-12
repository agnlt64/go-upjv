import os
from dotenv import load_dotenv

# Charge le fichier de variables du repo s'il existe (variables.env)
# Reprend le comportement normal de .env si un fichier .env existe ou si variables.env est absent
load_dotenv('variables.env')
load_dotenv()

DEV = 'development'
PROD = 'production'
DEFAULT = 'default'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Requiert DEV_DATABASE_URL, sinon raise an error
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class ProductionConfig(Config):
    DEBUG = False
    # Require DATABASE_URL, sinon raise an error
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    DEV: DevelopmentConfig,
    PROD: ProductionConfig,
    DEFAULT: DevelopmentConfig
}
