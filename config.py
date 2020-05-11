class config():
    DEBUG = False
    JWT_SECRET_KEY = 'super-secret'  # Change this!
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../DictionaryDB.db'
     
class devSet(config):
    DEBUG = True
    