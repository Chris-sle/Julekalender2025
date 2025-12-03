from app import create_app, db
from app.models import Admin

app = create_app()

with app.app_context():
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    # Sjekk om bruker finnes
    if Admin.query.filter_by(email=email).first():
        print("User already exists!")
    else:
        new_admin = Admin(email=email)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()
        print(f"Admin {email} created successfully!")