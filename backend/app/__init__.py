import os
from flask import Flask
from flask_redis import FlaskRedis
from config import Config, TestConfig


redis_store = FlaskRedis()


def create_app():
    app = Flask(__name__)
    config = TestConfig
    config_name = os.getenv('FLASK_CONFIG')
    if config_name:
        config = Config
    app.config.from_object(config)
    redis_store.init_app(app)
    from .service import bp
    app.register_blueprint(bp)
    counter = redis_store.get('counter')
    if not counter:
        redis_store.set('counter', int(1e7))
    return app
