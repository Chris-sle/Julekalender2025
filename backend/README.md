# Julekalender Backend 🎅

Dette er backend-API-et for Julekalender-applikasjonen 2025. Det er bygget med Flask og PostgreSQL, og håndterer administrasjon av luker, autentisering, og logging av besøkende.

## 🛠 Teknisk Stack

- **Språk:** Python 3
- **Rammeverk:** Flask
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Autentisering:** JWT (JSON Web Tokens)

## 📂 Mappestruktur

backend/
├── app/
│ ├── routes/ # API-endepunkter (auth, calendar)
│ ├── models.py # Databasemodeller
│ ├── utils.py # Hjelpefunksjoner (JWT, logging)
│ └── init.py # App-fabrikk og konfigurasjon
├── create_db.py # Script for å sette opp database og tabeller
├── create_admin.py # Script for å opprette første admin-bruker
├── run.py # Startfil for serveren
├── test_backend.py # Testscript som sjekker at alt virker
└── requirements.txt # Avhengigheter


## 🚀 Kom i gang

### 1. Forutsetninger
Sørg for at du har **Python** og **PostgreSQL** installert på maskinen din.

### 2. Installasjon
Lag et virtuelt miljø og installer avhengigheter:

Windows
python -m venv venv
venv\Scripts\activate

Mac/Linux
python3 -m venv venv
source venv/bin/activate

Installer pakker
pip install -r requirements.txt

### 3. Miljøvariabler (.env)
Lag en fil som heter `.env` i rotmappen og fyll inn følgende:

FLASK_APP=run.py
FLASK_ENV=development
FLASK_SECRET_KEY=din-hemmelige-flask-nokkel
JWT_SECRET_KEY=din-hemmelige-jwt-nokkel
JWT_EXPIRES_HOURS=12

Database URL (bytt ut passordet med ditt eget)
SQLALCHEMY_DATABASE_URI=postgresql://backend_user:s3curePa55code@localhost:5432/christmascalendar_db

### 4. Databaseoppsett
Kjør scriptet for å opprette database, bruker og tabeller automatisk. Du vil bli bedt om passordet til din lokale postgres-superbruker

python create_db.py


### 5. Opprett Admin-bruker
Siden systemet er låst for vanlige brukere, må du lage den første administratoren manuelt:

python create_admin.py *(Følg instruksjonene i terminalen for å velge e-post og passord)*


### 6. Start Serveren
python run.py

Serveren kjører nå på `http://localhost:5000`.

---

## 🧪 Testing
Du kan kjøre det inkluderte testscriptet for å verifisere at hele flyten fungerer (Login -> Opprett luke -> Besøk luke -> Slett luke).

1. Start serveren i ett terminalvindu (`python run.py`).
2. Kjør testen i et annet vindu:

python test_backend.py


---

## 📡 API Endepunkter

### Autentisering (Admin)
| Metode | Endepunkt | Beskrivelse | Body |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/login` | Logg inn og få token | `{"email": "...", "password": "..."}` |
| `POST` | `/auth/change-password` | Endre passord | `{"new_password": "..."}` (Krever Auth) |

### Kalender (Offentlig)
| Metode | Endepunkt | Beskrivelse | Headers |
| :--- | :--- | :--- | :--- |
| `GET` | `/calendar/<dato>` | Hent innhold for en luke | `X-Visitor-Token: <uuid>` (For logging) |

### Kalender (Admin) - Krever `Authorization: Bearer <token>`
| Metode | Endepunkt | Beskrivelse | Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/calendar` | List alle luker | - |
| `POST` | `/calendar` | Opprett ny luke | `{"date": "YYYY-MM-DD", "youtube_url": "...", ...}` |
| `PUT` | `/calendar/<id>` | Oppdater en luke | `{"task_text": "...", ...}` |
| `DELETE` | `/calendar/<id>` | Slett en luke | - |

---

## 📝 Notater
- **Besøkslogging:** Systemet bruker en UUID lagret i frontend (localStorage) som sendes med headeren `X-Visitor-Token` for å telle unike åpninger av luker anonymt.
- **Sikkerhet:** Passord hashes med Werkzeug før lagring.