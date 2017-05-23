import os


class Config:

    DEBUG = True
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = r'1\xc4ss\xcd;\xc4cC\x01\xf7\x8d\xfe,'
    TOKEN_LIFETIME = 43200  # 12 Hours
    APPLICATION_NAME = 'Export KMT documents to Google Drive'
    CLIENT_SECRET_FILE = BASE_DIR + '/google_client_secret.json'
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    LDAP_SERVER = 'ldap://192.168.8.2:389'
    LDAP_USER = r'aig\administrator'
    LDAP_PASSWORD = 'R@mayan1234'


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql://root:maria@aig2016@192.168.8.37/kmt_backend'


class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://debian-sys-maint:7TRmZyxh3geOystg@127.0.0.1/kmt_backend'


class Local(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/kmt_backend'


class CeleryConfig:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'






app_config = {
    'development': Development,
    'production': Production,
    'local': Local
}
