from flask import Blueprint, request, jsonify, g
from datetime import datetime
from app import db
from app.models import CalendarEntry
from app.utils import admin_required, log_guest_access_to_db

calendar_bp = Blueprint('calendar', __name__)

# --- PUBLIC ROUTES ---

@calendar_bp.route('/calendar/<date_str>', methods=['GET'])
def get_calendar_entry(date_str):
    # Henter en luke for en gitt dato. Logger besøk hvis token sendes med.
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Hent luke (kun hvis publisert!)
    entry = CalendarEntry.query.filter_by(date=target_date, is_published=True).first()
    
    if not entry:
        return jsonify({"message": "No content found for this date"}), 404

    # Hent token fra header: "X-Visitor-Token"
    visitor_token = request.headers.get("X-Visitor-Token")
    if visitor_token:
        log_guest_access_to_db(visitor_token, entry.id)

    return jsonify(entry.to_dict())


# --- ADMIN ROUTES ---

@calendar_bp.route('/calendar', methods=['GET'])
@admin_required
def list_all_entries():
    # Admin ser alt, også upublisert
    entries = CalendarEntry.query.order_by(CalendarEntry.date.asc()).all()
    return jsonify([e.to_dict() for e in entries])

@calendar_bp.route('/calendar', methods=['POST'])
@admin_required
def create_entry():
    data = request.get_json()
    
    try:
        entry_date = datetime.strptime(data.get('date'), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid date"}), 400

    if CalendarEntry.query.filter_by(date=entry_date).first():
        return jsonify({"message": "Entry already exists for this date"}), 400

    new_entry = CalendarEntry(
        date=entry_date,
        youtube_url=data.get('youtube_url'),
        task_text=data.get('task_text'),
        video_type=data.get('video_type', 'youtube'),
        is_published=data.get('is_published', False),
        created_by=g.current_admin.id
    )
    
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify(new_entry.to_dict()), 201

@calendar_bp.route('/calendar/<int:id>', methods=['PUT'])
@admin_required
def update_entry(id):
    entry = db.session.get(CalendarEntry, id)
    if not entry:
        return jsonify({"message": "Not found"}), 404
        
    data = request.get_json()
    
    if 'youtube_url' in data: entry.youtube_url = data['youtube_url']
    if 'task_text' in data: entry.task_text = data['task_text']
    if 'is_published' in data: entry.is_published = data['is_published']
    
    db.session.commit()
    return jsonify(entry.to_dict())

@calendar_bp.route('/calendar/<int:id>', methods=['DELETE'])
@admin_required
def delete_entry(id):
    entry = db.session.get(CalendarEntry, id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return jsonify({"message": "Deleted"})