from flask import Blueprint, request, jsonify, g
from datetime import datetime
from werkzeug.utils import secure_filename
from app import db
from app.models import CalendarEntry, AccessLog
from app.utils import admin_required, log_guest_access_to_db
import os

calendar_bp = Blueprint('calendar', __name__)

# Use an absolute uploads folder (backend/uploads) to avoid relative-path issues
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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
    form = request.form

    try:
        entry_date = datetime.strptime(form.get("date"), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid date"}), 400

    if CalendarEntry.query.filter_by(date=entry_date).first():
        return jsonify({"message": "Entry already exists for this date"}), 400

    video_type = form.get("video_type", "upload")
    video_path = None

    if video_type == "upload":
        files = request.files.getlist("files")
        if not files or not files[0].filename:
            return jsonify({"message": "Ingen fil lastet opp"}), 400
        f = files[0]
        filename = secure_filename(f.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(save_path)
        video_path = save_path

    elif video_type == "youtube":
        youtube_url = form.get("youtube_url", "").strip()
        if not youtube_url:
            return jsonify({"message": "YouTube-lenke mangler"}), 400
        video_path = youtube_url  # lagre lenken direkte i video_path

    else:
        return jsonify({"message": "Ugyldig video_type"}), 400

    new_entry = CalendarEntry(
        date=entry_date,
        task_text=form.get("task_text"),
        video_type=video_type,
        video_path=video_path,           # ← her havner enten filsti eller YouTube-lenke
        is_published=form.get("is_published") == "true",
        created_by=g.current_admin.id
    )

    db.session.add(new_entry)
    db.session.commit()

    return jsonify(new_entry.to_dict()), 201


# -----------------------------
# ADMIN: UPDATE ENTRY (JSON)
# -----------------------------
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


# -----------------------------
# ADMIN: DELETE ENTRY
# -----------------------------
@calendar_bp.route('/calendar/<int:entry_id>', methods=['DELETE'])
@admin_required
def delete_calendar_entry(entry_id):
    entry = db.session.get(CalendarEntry, entry_id)

    if not entry:
        return jsonify({"message": "Not found"}), 404

    # Slett tilknyttede access logs først
    AccessLog.query.filter_by(calendar_id=entry.id).delete()
    
    # Slett kalenderluken
    db.session.delete(entry)
    db.session.commit()

    return jsonify({"message": "Deleted"})
