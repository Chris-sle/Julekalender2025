from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# Initialiser utvidelser globalt, men uten app context ennå
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Koble utvidelser til appen
    db.init_app(app)

    # Registrer Blueprints (ruter)
    from app.routes.auth import auth_bp
    from app.routes.calendar import calendar_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(calendar_bp)

    return app