from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.routes.index import index_p
from app.routes.auth import auth
from app.routes.post import post_router


def suma(a, b):
    return a + b


def create_app():
    app = Flask(__name__)

    # multiple blueprints
    app.register_blueprint(index_p)
    app.register_blueprint(auth)
    app.register_blueprint(post_router)

    Bootstrap(app)
    app.config.from_object(Config)

    db = SQLAlchemy(app)
    Migrate(app, db)

    return app
