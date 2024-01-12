from flask import Flask
from app.chat import chat
from app.videos import videos_functions
from config import Config 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
import sqlalchemy as sa
import os
from elasticsearch import Elasticsearch
from logging.handlers import SMTPHandler,RotatingFileHandler
from app.extensions import db
from flask_cors import CORS
from app.maps.hospital_filter import get_top
migrate = Migrate()
login = LoginManager()
cors =CORS()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    cors.init_app(app)
    with app.app_context():
        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp,url_prefix='/auth')
        from app.main import bp as main_bp
        app.register_blueprint(main_bp)
        from app.api import bp as api_bp
        app.register_blueprint(api_bp,url_prefix='/api')
        from app.cli import bp as cli_bp
        app.register_blueprint(cli_bp)
        from app.chat import bp as chat_bp
        app.register_blueprint(chat_bp)
        from app.videos import bp as videos_bp
        app.register_blueprint(videos_bp)
        from app.maps import bp as maps_bp
        app.register_blueprint(maps_bp)
        
    app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL']) if app.config['ELASTICSEARCH_URL'] else None
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("user"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'],app.config['MAIL_PORT']),
                fromaddr='no-reply@'+app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'],
                subject='App Error Alert',
                credentials=auth,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log',maxBytes=10240,backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s : %(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('hub_startup')




    return app

from app import models



