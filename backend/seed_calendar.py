import os
import sys
import getpass
from datetime import date
import requests
from dotenv import load_dotenv

# Last .env
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000").rstrip("/")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def prompt_if_missing():
    global ADMIN_EMAIL, ADMIN_PASSWORD

    if not ADMIN_EMAIL:
        ADMIN_EMAIL = input("Admin e-post: ").strip()
    if not ADMIN_PASSWORD:
        ADMIN_PASSWORD = getpass.getpass("Admin passord: ").strip()

def login():
    url = f"{API_BASE_URL}/auth/login"
    resp = requests.post(url, json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    if resp.status_code != 200:
        print(f"Login feilet ({resp.status_code}): {resp.text}")
        sys.exit(1)
    data = resp.json()
    token = data.get("access_token")
    if not token:
        print("Fikk ikke access_token fra backend:", data)
        sys.exit(1)
    print("Login OK.")
    return token

def build_episodes():
    base_year = 2025

    urls = {
        1: "https://www.youtube.com/watch?v=bFHy61erVyQ&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8index=1",
        2: "https://www.youtube.com/watch?v=OaUoWeBbYAo&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=2",
        3: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=3",
        4: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=4",
        5: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=5",
        6: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=6",
        7: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=7",
        8: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=8",
        9: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=9",
        10: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=10",
        11: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=11",
        12: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=12",
        13: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=13",
        14: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=14",
        15: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=15",
        16: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=16",
        17: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=17",
        18: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=18",
        19: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=19",
        20: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=20",
        21: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=21",
        22: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=22",
        23: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=23",
        24: "https://www.youtube.com/watch?v=qBegaNpUp7o&list=PLCRckkFYzeCBmwjeMzP7oTKeXWebpZlM8&index=24",
    }

    texts = {
        1: "Ved verdens ende får tre nisser et alvorlig oppdrag som gjør at både julestemning og fare plutselig henger sammen.",
        2: "Reisen mot Trøndelag byr på uventede problemer, og det går opp for nissene at veien til nøkkelen blir mer humpete enn planlagt.",
        3: "På en rolig potetgård i Sør-Trøndelag aner et ektepar at hverdagen er i ferd med å forandre seg, uten at de helt forstår hvorfor.",
        4: "En fremmed mann banker på døra til gården og presenterer seg høflig, men både væremåte og forklaringer skurrer fra første stund.",
        5: "Nissene prøver å få kontroll på situasjonen etter en hard landing, mens den nye gjesten på gården finner gode grunner til å bli litt lenger.",
        6: "Avstanden mellom nisser og mennesker krymper når sporene etter noe uvanlig blir tydeligere både i lufta og rundt gårdstunet.",
        7: "Et praktisk problem tvinger nissene til tålmodig håndverk, og oppdraget stopper opp mens tiden ubehagelig nok tikker mot jul.",
        8: "På gården Sand blir misforståelser og rare formuleringer flere, og det er tydelig at gjesten ikke bare er interessert i poteter.",
        9: "Nissene kommer nærmere stedet de leter etter, men innser at selv en «enkel» hule kan skjule mer enn de hadde sett for seg.",
        10: "Den merkelige gjesten begynner å stille stadig mer spesifikke spørsmål, og nysgjerrigheten hans får en skarpere kant.",
        11: "Magiske hjelpemidler viser seg nyttige, men også sårbare, og nissene må passe ekstra godt på det de har fått betrodd.",
        12: "Spenningen på gården øker når små detaljer avslører at noen ikke er helt den han utgir seg for å være.",
        13: "Nissene opplever at selv en trygg hule ikke nødvendigvis er trygg når andre også begynner å fatte interesse for den.",
        14: "Forsøk på å opptre normalt på gården blir stadig mer komiske i møte med Norwenglish, misforståelser og skjulte motiver.",
        15: "En viktig gjenstand skifter hender, og balansen mellom nisser, mennesker og den fremmede blir merkbart mer urolig.",
        16: "Følgene av feil person med feil bok begynner å merkes, og det blir tydelig hvor farlig kunnskap kan være i gale hender.",
        17: "Nissene må tenke mer kreativt enn noen gang for å rette opp i skaden som er gjort, mens klokka mot jul går stadig fortere.",
        18: "Stemningen mørkner når makt og magi blandes med grådighet, men humoren holder seg i språket og de små, rare hverdagssituasjonene.",
        19: "På gården presses både gjestfrihet og tålmodighet til bristepunktet, og ekteparet aner at noe stort holdes skjult for dem.",
        20: "Nissene nærmer seg endelig målet for turen, men oppdager at nøkkelen til å lykkes ikke bare handler om å finne en fysisk gjenstand.",
        21: "Følelser og savn får større plass, og musikken knyttes tettere til det som står på spill for både nissene og menneskene rundt dem.",
        22: "Alle parter forbereder seg på det som skal skje, noen med planer de tror er smarte, andre med håp om at ting endelig skal ordne seg.",
        23: "Spenningen topper seg når hemmeligheter avdekkes, og konsekvensene av valgene som er tatt ikke lenger kan skyves foran seg.",
        24: "På selveste julaften knyttes trådene sammen rundt nøkkelen, musikkboksen og Gammel Nok, og det blir klart hva julen egentlig kommer til å bety for alle.",
    }

    episodes = []
    for day in range(1, 25):
        episodes.append(
            {
                "day": day,
                "date": date(base_year, 12, day).isoformat(),
                "youtube_url": urls[day],
                "text": texts[day],
            }
        )
    return episodes

def create_entries(token, episodes):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{API_BASE_URL}/calendar"

    for ep in episodes:
        data = {
            "date": ep["date"],
            "task_text": ep["text"],
            "video_type": "youtube",
            "youtube_url": ep["youtube_url"],
            "is_published": "true",
        }

        print(f"Oppretter luke {ep['day']} ({ep['date']}) ...", end=" ")
        resp = requests.post(url, headers=headers, data=data)
        if resp.status_code == 201:
            print("OK")
        else:
            try:
                msg = resp.json()
            except Exception:
                msg = resp.text
            print(f"FEIL [{resp.status_code}]: {msg}")

def main():
    print(f"Bruker API_BASE_URL={API_BASE_URL}")
    prompt_if_missing()
    token = login()
    episodes = build_episodes()
    create_entries(token, episodes)
    print("Ferdig.")

if __name__ == "__main__":
    main()