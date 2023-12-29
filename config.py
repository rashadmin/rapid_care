import os
basedir = os.path.abspath(os.path.dirname(__name__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ayom0908'
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'app.db')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['abdul.a.rasheed2022@gmail.com']
    CHAT_PER_PAGE = 5
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')
    