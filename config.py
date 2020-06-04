"""
Configuration file
"""


class Config():
    """General configuration"""
    DEBUG = False
    JWT_SECRET_KEY = 'The-Secret-key'  # To be changed
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'


class DevSet(Config):
    """Configuration for the dev environment"""
    DEBUG = True
