from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    from config import Config
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # Importación del Blueprint
    from app.interfaces.web.controllers import bp
    app.register_blueprint(bp)
    
    with app.app_context():
        db.create_all()
    
    return app