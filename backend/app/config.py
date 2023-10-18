import os

class BaseConfig(object):
    PROJECT = "app"

    PROJECT_ROOT = os.path.dirname(__file__)

    DEBUG = False
    TESTING = False

    ADMINS = ["peep12ng@gmail.com"]

class DefaultConfig(BaseConfig):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mariadb+pymysql://hotdeal:Qlalfqjsgh!23@sdavids.synology.me:3306/hotdeal"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalConfig(DefaultConfig):
    pass

class StagingConfig(DefaultConfig):
    pass

class ProdConfig(DefaultConfig):
    pass

def get_config(MODE):
    SWITCH = {
        "LOCAL":LocalConfig,
        "STAGING":StagingConfig,
        "PRODUCTION":ProdConfig,
    }