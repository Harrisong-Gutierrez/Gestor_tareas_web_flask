from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets  # Importamos el módulo secrets para generar una clave segura

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    from config import Config

    app.config.from_object(Config)

    app.secret_key = secrets.token_hex(32)

    db.init_app(app)

    from app.interfaces.web.controllers import bp

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
