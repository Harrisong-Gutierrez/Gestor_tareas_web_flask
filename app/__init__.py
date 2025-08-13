from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import secrets

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.secret_key = secrets.token_hex(32)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes import bp

    app.register_blueprint(bp)

    return app
