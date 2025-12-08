from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config

# Initialiser utvidelser globalt, men uten app context ennå
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Koble utvidelser til appen
    db.init_app(app)

    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Registrer Blueprints (ruter)
    from app.routes.auth import auth_bp
    from app.routes.calendar import calendar_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(calendar_bp)

    return app

