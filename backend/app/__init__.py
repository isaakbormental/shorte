from flask import Flask
from flask_redis import FlaskRedis
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
redis_store = FlaskRedis(app)

from app import views

counter = redis_store.get('counter')
if not counter:
    redis_store.set('counter', int(1e7))
