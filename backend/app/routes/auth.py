from flask import Blueprint, request, jsonify, g
from datetime import datetime
from app import db
from app.models import Admin
from app.utils import create_admin_token, admin_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    admin = Admin.query.filter_by(email=email).first()
    
    if not admin or not admin.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Oppdater last_login
    admin.last_login = datetime.utcnow()
    db.session.commit()

    token = create_admin_token(admin.id, admin.email)
    return jsonify({"access_token": token})

@auth_bp.route('/auth/change-password', methods=['POST'])
@admin_required
def change_password():
    data = request.get_json()
    new_password = data.get("new_password")
    
    if not new_password:
        return jsonify({"message": "New password required"}), 400
        
    admin = g.current_admin
    admin.set_password(new_password)
    db.session.commit()
    
    return jsonify({"message": "Password updated successfully"})