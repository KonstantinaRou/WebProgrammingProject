class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://konstantina:1234@localhost/ecv_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True #gia na anixneyei allages sthn vash poy exoyn ginei apo ton xhsth
    SECRET_KEY = 'I love burgers' #kleidi gia kryptografish
    WOLFRAM_KEY = 'QE6QR4-XLP29T6PTG'
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True