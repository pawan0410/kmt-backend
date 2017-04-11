import os


class Config:

    DEBUG = True
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = r'1\xc4ss\xcd;\xc4cC\x01\xf7\x8d\xfe,'
    TOKEN_LIFETIME = 43200  # 12 Hours
    APPLICATION_NAME = 'Export KMT documents to Google Drive'
    CREDENTIALS_PATH = BASE_DIR + '/drive/drive-credentials.json'
    CLIENT_SECRET_PATH = BASE_DIR + '/google_client_secret.json'
    DRIVE_FOLDER_ID = '0B9DrzugQJ4wAakRBbFNjbTlkcFE'


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql://root:root@127.0.0.1/kmt_backend'


class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root@127.0.0.1/kmt_backend'


app_config = {
    'development': Development,
    'production': Production
}