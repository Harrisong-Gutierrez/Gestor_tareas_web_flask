from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuración desde el archivo config.py
    app.config.from_object('config.Config')
    
    # Registrar blueprints
    from app.routes import bp
    app.register_blueprint(bp)

    return app