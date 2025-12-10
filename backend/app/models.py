from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class CalendarEntry(db.Model):
    __tablename__ = "calendarentries"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    youtube_url = db.Column(db.String(255))
    task_text = db.Column(db.Text)
    video_type = db.Column(db.String(10)) # 'youtube' eller 'upload'
    video_path = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey("admins.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    is_published = db.Column(db.Boolean, default=False)

    def to_dict(self):
        import os  # Importer os her inne for sikkerhets skyld
        
        video_url = None
        if self.video_type == "youtube":
            video_url = self.video_path # YouTube lenken lagres direkte i video_path nå
        elif self.video_type == "upload" and self.video_path:
            # Backend-ruten '/uploads/<filename>' serverer filene
            filename = os.path.basename(self.video_path)
            video_url = f"/uploads/{filename}"

        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "task_text": self.task_text,
            "video_type": self.video_type,
            "video_path": self.video_path, # Behold for referanse
            "video_url": video_url,        # <--- NYTT: Brukes av frontend for å vise videoen!
            "is_published": self.is_published
        }

class Visitor(db.Model):
    __tablename__ = "visitors"
    # Bruker UUID som primærnøkkel
    token_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_visit = db.Column(db.DateTime, server_default=db.func.now())

class AccessLog(db.Model):
    __tablename__ = "accesslogs"

    id = db.Column(db.Integer, primary_key=True)
    visitor_token = db.Column(UUID(as_uuid=True), db.ForeignKey("visitors.token_id"))
    calendar_id = db.Column(db.Integer, db.ForeignKey("calendarentries.id"))
    access_time = db.Column(db.DateTime, server_default=db.func.now())
