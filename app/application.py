import locale
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.contrib.fixers import ProxyFix

from flask import Flask

from app.config import app_config
from app.extension import db
from app.extension import api
from app.extension import jwt
from app.extension import cors
from app.default.views import default_blueprint
from app.api.auth import Auth
from app.api.auth import Validate
from app.api.documents import Documents
from app.api.documents import DocumentsList


def application(config):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_object(app_config[config])

    handler = RotatingFileHandler('backend.log')
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Register Blueprint
    app.register_blueprint(default_blueprint)

    api.add_resource(Auth, '/v1/auth/')
    api.add_resource(Validate, '/v1/auth/validate')
    api.add_resource(DocumentsList, '/v1/documents/')
    api.add_resource(Documents, '/v1/documents/<int:id>')

    # Register Extensions
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
    with app.app_context():
        db.create_all()
    return app