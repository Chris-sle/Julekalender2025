import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import getpass

# Hent inn brukernavn/passord fra terminalen
print("--- Julekalender Database Setup ---")
print("Du trenger en superbruker (vanligvis 'postgres') for å opprette databasen.")
pg_user = input("Superbruker (default 'postgres'): ") or "postgres"
pg_password = getpass.getpass("Passord for superbruker: ")
pg_host = input("Host (default 'localhost'): ") or "localhost"
pg_port = input("Port (default '5432'): ") or "5432"

# Navn på ny database og ny bruker
NEW_DB_NAME = "christmascalendar_db"
NEW_USER = "backend_user"
NEW_USER_PASS = "s3curePa55code"

# SQL for å slette database/bruker hvis de finnes (RESET) - Valgfritt, men nyttig under testing
DROP_EXISTING = True 

def get_conn(db_name=None):
    #Hjelpefunksjon for å koble til
    return psycopg2.connect(
        user=pg_user,
        password=pg_password,
        host=pg_host,
        port=pg_port,
        dbname=db_name if db_name else "postgres"
    )

try:
    # -------------------------------------------------------
    # 1. Koble til 'postgres' for å lage selve databasen
    # -------------------------------------------------------
    print(f"\nKobler til server som '{pg_user}'...")
    conn = get_conn()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    if DROP_EXISTING:
        print(f"Sletter eksisterende database '{NEW_DB_NAME}' (hvis den finnes)...")
        cur.execute(f"DROP DATABASE IF EXISTS {NEW_DB_NAME};")
        print(f"Sletter eksisterende bruker '{NEW_USER}' (hvis den finnes)...")
        cur.execute(f"DROP ROLE IF EXISTS {NEW_USER};")

    # Sjekk om database finnes, hvis ikke opprett den
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{NEW_DB_NAME}';")
    if not cur.fetchone():
        print(f"Oppretter database '{NEW_DB_NAME}'...")
        cur.execute(f"CREATE DATABASE {NEW_DB_NAME};")
    else:
        print(f"Databasen '{NEW_DB_NAME}' finnes allerede.")

    # Opprett brukeren, eller hopp over hvis den finnes
    print(f"Oppretter/oppdaterer bruker '{NEW_USER}'...")
    try:
        cur.execute(f"CREATE ROLE {NEW_USER} WITH LOGIN PASSWORD '{NEW_USER_PASS}';")
    except psycopg2.errors.DuplicateObject:
        print(f"Bruker '{NEW_USER}' fantes allerede, hopper over oppretting.")
    
    cur.close()
    conn.close()

    # -------------------------------------------------------
    # 2. Koble til den NYE databasen for å lage tabeller
    # -------------------------------------------------------
    print(f"\nKobler til '{NEW_DB_NAME}' for å opprette tabeller...")
    conn = get_conn(db_name=NEW_DB_NAME)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # Viktig for noen rettighets-kommandoer
    cur = conn.cursor()

    # --- SQL DEFINISJONER ---
    table_queries = [
        """
        CREATE TABLE Admins (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            last_login TIMESTAMP
        );
        """,
        """
        CREATE TABLE CalendarEntries (
            id SERIAL PRIMARY KEY,
            date DATE UNIQUE NOT NULL,
            youtube_url VARCHAR(255),
            task_text TEXT,
            video_type VARCHAR(10) CHECK (video_type IN ('youtube', 'upload')),
            video_path VARCHAR(255),
            created_by INTEGER REFERENCES Admins(id),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            is_published BOOLEAN DEFAULT FALSE
        );
        """,
        """
        CREATE TABLE Visitors (
            token_id UUID PRIMARY KEY,
            first_visit TIMESTAMP DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE AccessLogs (
            id SERIAL PRIMARY KEY,
            visitor_token UUID REFERENCES Visitors(token_id),
            calendar_id INTEGER REFERENCES CalendarEntries(id),
            access_time TIMESTAMP DEFAULT NOW()
        );
        """
    ]

    print("Oppretter tabeller...")
    for query in table_queries:
        cur.execute(query)

    # --- RETTIGHETER ---
    print(f"Gir rettigheter til '{NEW_USER}'...")
    
    # Merk: Vi er inne i 'christmascalendar_db' nå, så GRANT gjelder her.
    permissions = [
        f"GRANT CONNECT ON DATABASE {NEW_DB_NAME} TO {NEW_USER};",
        f"GRANT USAGE ON SCHEMA public TO {NEW_USER};",
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {NEW_USER};",
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {NEW_USER};",
        f"GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO {NEW_USER};",
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO {NEW_USER};",
    ]

    for perm in permissions:
        cur.execute(perm)

    print("\n✅ Ferdig! Databasen er satt opp og klar til bruk.")
    print(f"Husk å oppdatere .env filen din med passordet: {NEW_USER_PASS}")

except Exception as e:
    print(f"\n❌ En feil oppstod: {e}")
finally:
    if 'cur' in locals() and cur: cur.close()
    if 'conn' in locals() and conn: conn.close()