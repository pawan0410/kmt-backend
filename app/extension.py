from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery
from app.config import CeleryConfig

db = SQLAlchemy()
api = Api()
jwt = JWTManager()
cors = CORS()
task_server = Celery(__name__, broker=CeleryConfig.CELERY_BROKER_URL)
task_server.config_from_object(CeleryConfig)
