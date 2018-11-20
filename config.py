# config.py


class Config:

    def init_app(app):
        pass 


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "dbname='sendit' host='localhost' port='5432'\
                    user='eric' password='hardpassword'"


class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = "dbname='sendit-tests' host='localhost' port='5432'\
                    user='eric' password='hardpassword'"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
