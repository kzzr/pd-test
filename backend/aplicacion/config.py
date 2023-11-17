class Config(object):
    SECRET_KEY = 'f0faa2bed03b28e48544762d760aa169'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_POOL_RECYCLE = 300
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REDIS_URL = "redis://@redis:6379/0"
    URL_API = "https://api.pagerduty.com"
    TOKEN_PD = "u+MYysWbvYXHCZu497xg"
    

class TestingConfig(Config):
    """
    Testing configurations
    """
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_POOL_RECYCLE = 300
    TESTING = True 
    DEBUG = True
    REDIS_URL = "redis://@redis:6379/0"
    URL_API = "https://api.pagerduty.com"
    TOKEN_PD = "u+MYysWbvYXHCZu497xg"
    

class ProductionConfig(Config):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_POOL_RECYCLE = 300
    REDIS_URL = "redis://@redis:6379/0"
    URL_API = "https://api.pagerduty.com"
    TOKEN_PD = "u+MYysWbvYXHCZu497xg"
    

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
