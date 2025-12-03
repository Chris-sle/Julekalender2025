from functools import wraps
from flask import request, jsonify, g, current_app
import jwt
from datetime import datetime, timedelta
import uuid
from app import db
from app.models import Admin, Visitor, AccessLog

def create_admin_token(admin_id, email):
    payload = {
        "sub": str(admin_id),
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=current_app.config["JWT_EXPIRES_HOURS"]),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid Authorization header"}), 401
        
        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError as e:
            print(f"DEBUG: Feilen er: {e}")
            return jsonify({"message": "Invalid token"}), 401

        user = db.session.get(Admin, payload.get("sub")) # Nyere SQLAlchemy syntaks
        if not user:
            return jsonify({"message": "Admin not found"}), 401

        g.current_admin = user
        return f(*args, **kwargs)

    return wrapper

def log_guest_access_to_db(token_uuid_str, calendar_entry_id):
    # Logger besøk. Oppretter Visitor hvis den ikke finnes.
    if not token_uuid_str:
        return

    try:
        # Konverter string til UUID objekt
        token_uuid = uuid.UUID(token_uuid_str)
    except ValueError:
        return # Ugyldig UUID, vi logger ikke

    # Sjekk om visitor finnes, hvis ikke lag ny
    visitor = db.session.get(Visitor, token_uuid)
    if not visitor:
        visitor = Visitor(token_id=token_uuid)
        db.session.add(visitor)
        # Flush for å sikre at visitor eksisterer før vi lager logg entry
        db.session.flush() 

    # Logg selve åpningen av luken
    access = AccessLog(visitor_token=token_uuid, calendar_id=calendar_entry_id)
    db.session.add(access)
    db.session.commit()