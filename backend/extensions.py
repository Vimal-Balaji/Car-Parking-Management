import redis
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import *

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)
red=redis.Redis(host='localhost', port=6379, db=0)