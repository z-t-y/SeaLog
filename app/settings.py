# flake8: noqa
import os
from flask import Flask
from flask_babel import lazy_gettext as _l
from werkzeug.security import generate_password_hash


def generate_sqlite_file(filename: str):
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return 'sqlite:///' + os.path.join(basedir, f'{filename}.sqlite3')


class Base:
    DEBUG = False
    TESTING = False
    SSL_REDIRECT = False

    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("FLOG_EMAIL")
    MAIL_PASSWORD = os.getenv("FLOG_EMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("DEFAULT_EMAIL_SENDER")

    ADMIN_NAME = os.getenv('FLOG_ADMIN_NAME')
    ADMIN_EMAIL = MAIL_USERNAME
    ADMIN_EMAIL_LIST = [ADMIN_EMAIL]
    ADMIN_PASSWORD = os.getenv('FLOG_ADMIN_PASSWORD')

    # ('theme name': 'display name')
    BOOTSTRAP_THEMES = {'default': _l('Default'), 'lite': _l('Lite'), 'dark': _l('Dark')}

    POSTS_PER_PAGE = 8
    USERS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 10
    NOTIFICATIONS_PER_PAGE = 10

    LOCALES = {
        'en_US': 'English(US)',
        'zh_Hans_CN': '简体中文'
    }

    @classmethod
    def init_app(cls, app):
        pass


class Production(Base):
    FLASK_CONFIG = 'production'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", generate_sqlite_file('data'))

    @classmethod
    def init_app(cls, app):
        Base.init_app(app)
        
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'ADMIN_EMAIL', None) is not None:
            credentials = (cls.ADMIN_EMAIL, cls.ADMIN_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.DEFAULT_EMAIL_SENDER,
            toaddrs=[cls.ADMIN_EMAIL],
            subject='Application Error',
            credentials=credentials, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        


class Development(Base):
    FLASK_CONFIG = 'development'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_DEV', generate_sqlite_file('data-dev'))
    DEBUG = True
    MAIL_SUPPRESS_SEND = False
    ADMIN_EMAIL_LIST = [os.getenv("ADMIN_EMAIL")]


class Test(Base):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    MAIL_DEFAULT_SENDER = os.getenv("DEFAULT_EMAIL_SENDER")
    ADMIN_EMAIL_LIST = [os.getenv("ADMIN_EMAIL")]


class Heroku(Production):
    SSL_REDIRECT = True if os.getenv('DYNO') else False
    @classmethod
    def init_app(cls, app: Flask):
        Production.init_app(app)
        
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)


config = {
    'production': Production,
    'development': Development,
    'testing': Test,
    'heroku': Heroku
}
