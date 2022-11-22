from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.routes.post import post_router
from app.routes.auth import auth_router
from app.routes.index import index_router


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(Config)

    app.register_blueprint(post_router)
    app.register_blueprint(auth_router)
    app.register_blueprint(index_router)

    db = SQLAlchemy(app)
    Migrate(app, db)

    return app
