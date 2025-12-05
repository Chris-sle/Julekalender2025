import requests
import uuid
import sys
from datetime import datetime
from app import create_app, db
from app.models import Admin, CalendarEntry, Visitor, AccessLog

# --- KONFIGURASJON ---
BASE_URL = "http://localhost:5000"
TEST_EMAIL = "testadmin@example.com"
TEST_PASS = "testpassword123"
TEST_DATE = "2025-12-24"

def setup_test_data():
    print("[SETUP] Oppretter test-admin i databasen...")
    app = create_app()
    with app.app_context():
        # 1. Finn admin
        existing = Admin.query.filter_by(email=TEST_EMAIL).first()
        
        if existing:
            print(f"[SETUP] Fant eksisterende admin (ID: {existing.id}). Rydder opp...")
            
            try:
                # sletter manuelt i riktig rekkefølge for å unngå foreign key error
                # 1. Slett logger knyttet til luker laget av denne admin
                
                # Hent ID-ene til lukene denne adminen eier
                calendar_ids = [e.id for e in CalendarEntry.query.filter_by(created_by=existing.id).all()]
                
                if calendar_ids:
                    # Slett AccessLogs for disse lukene
                    AccessLog.query.filter(AccessLog.calendar_id.in_(calendar_ids)).delete(synchronize_session=False)
                    
                    # Slett selve lukene
                    CalendarEntry.query.filter(CalendarEntry.id.in_(calendar_ids)).delete(synchronize_session=False)
                
                # Commit sletting av barn FØR vi sletter admin
                db.session.commit()
                
                # 2. Nå sletter vi admin
                db.session.delete(existing)
                db.session.commit()
                print("[SETUP] Gammel data slettet.")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Feil under opprydding: {e}")
                # prøver å fortsette likevel, kanskje det går bra hvis admin ikke ble slettet
        
        # Sjekk om admin faktisk ble borte
        if not Admin.query.filter_by(email=TEST_EMAIL).first():
            # 3. Lag ny admin
            admin = Admin(email=TEST_EMAIL)
            admin.set_password(TEST_PASS)
            db.session.add(admin)
            db.session.commit()
            print("[SETUP] Ny Test-admin opprettet.")
        else:
            print("[SETUP] Gjenbruker eksisterende admin.")

def run_tests():
    session = requests.Session()
    
    # 1. LOGIN
    print("\n--- 1. Tester Login ---")
    login_payload = {"email": TEST_EMAIL, "password": TEST_PASS}
    response = session.post(f"{BASE_URL}/auth/login", json=login_payload)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"✅ Login suksess! Token mottatt.")
    else:
        print(f"❌ Login feilet: {response.text}")
        sys.exit(1)

    # Header for admin-kall
    auth_headers = {"Authorization": f"Bearer {token}"}
    print(f"DEBUG: Bruker token: {token}")

    # 2. OPPRETT KALENDERLUKE (ADMIN)
    print("\n--- 2. Tester Opprettelse av Kalenderluke ---")
    # Slett gammel luke for denne datoen først (for sikkerhets skyld)
    # Vi gjør dette via API hvis mulig, men her antar vi clean slate eller håndterer feil
    
    entry_payload = {
        "date": TEST_DATE,
        "youtube_url": "https://youtu.be/dQw4w9WgXcQ",
        "task_text": "God jul! Her er en sang.",
        "video_type": "youtube",
        "is_published": True
    }
    
    res = session.post(f"{BASE_URL}/calendar", json=entry_payload, headers=auth_headers)
    
    if res.status_code == 201:
        entry_id = res.json().get("id")
        print(f"✅ Kalenderluke opprettet for {TEST_DATE} (ID: {entry_id})")
    elif res.status_code == 400 and "already exists" in res.text:
        print(f"⚠️ Luken finnes allerede, fortsetter...")
        # Vi må finne ID-en til den eksisterende luken for å teste videre
        res_list = session.get(f"{BASE_URL}/calendar", headers=auth_headers)
        for entry in res_list.json():
            if entry["date"] == TEST_DATE:
                entry_id = entry["id"]
                break
    else:
        print(f"❌ Feilet å opprette luke: {res.text}")
        sys.exit(1)

    # 3. BESØK LUKE SOM GJEST (PUBLIC)
    print("\n--- 3. Tester Gjestebesøk og Logging ---")
    guest_token = str(uuid.uuid4())
    guest_headers = {"X-Visitor-Token": guest_token}
    
    res = session.get(f"{BASE_URL}/calendar/{TEST_DATE}", headers=guest_headers)
    
    if res.status_code == 200:
        data = res.json()
        print(f"✅ Gjest fikk innhold: {data.get('task_text')}")
    else:
        print(f"❌ Gjest fikk feil: {res.text}")

    # 4. VERIFISER LOGGING I DB
    print("\n--- 4. Verifiserer Database-logg ---")
    app = create_app()
    with app.app_context():
        # Sjekk om det finnes en loggføring for denne tokenen
        log_entry = AccessLog.query.join(Visitor).filter(Visitor.token_id == guest_token).first()
        if log_entry:
            print(f"✅ Loggføring funnet i databasen! (Visitor: {log_entry.visitor_token}, Time: {log_entry.access_time})")
        else:
            print("❌ Ingen loggføring funnet for denne gjesten.")

    # 5. SLETT KALENDERLUKE (CLEANUP)
    print("\n--- 5. Tester Sletting (Cleanup) ---")
    res = session.delete(f"{BASE_URL}/calendar/{entry_id}", headers=auth_headers)
    if res.status_code == 200:
        print("✅ Kalenderluke slettet.")
    else:
        print(f"❌ Sletting feilet: {res.text}")

if __name__ == "__main__":
    try:
        # Sjekk om server kjører først
        requests.get(BASE_URL)
        setup_test_data()
        run_tests()
        print("\n🎉 Alle tester fullført!")
    except requests.exceptions.ConnectionError:
        print(f"❌ Klarte ikke koble til {BASE_URL}. Kjører serveren?")
        print("   Husk å kjøre 'python run.py' i et annet vindu først.")