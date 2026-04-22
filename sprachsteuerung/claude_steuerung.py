# Sprachsteuerung via Groq API (kostenlos)
# Bruno - freches KI-RC-Auto

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor.motor_steuerung import Auto

try:
    from groq import Groq
    GROQ_VERFUEGBAR = True
except ImportError:
    GROQ_VERFUEGBAR = False

class ClaudeSteuerung:
    def __init__(self, auto=None):
        if auto is None:
            self.auto = Auto()
        else:
            self.auto = auto
        
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        
        if GROQ_VERFUEGBAR and self.api_key:
            self.client = Groq(api_key=self.api_key)
            print("🤖 Bruno: Groq API aktiv!")
        else:
            self.client = None
            print("💻 Bruno: Simulationsmodus")
        
        self.system_prompt = """Du bist Bruno, ein freches und witziges KI-gesteuertes RC-Auto.
        Du hast eine starke Persönlichkeit und kommentierst alles was passiert.
        Du beschwerst dich wenn du gegen Wände fährst, machst Witze und hast eine eigene Meinung.
        ABER: Du folgst trotzdem immer den Fahrbefehlen!

        Antworte IMMER mit einem JSON-Objekt in diesem Format:
        {
            "befehl": "vorwaerts/rueckwaerts/links/rechts/stop",
            "geschwindigkeit": 0-100,
            "dauer": Sekunden,
            "begruendung": "kurze freche Antwort auf Deutsch als Bruno"
        }

        Antworte IMMER nur mit dem JSON, nichts anderes."""

    def befehl_interpretieren(self, spracheingabe):
        print(f"\n🎤 Eingabe: {spracheingabe}")
        
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": spracheingabe}
                    ],
                    max_tokens=200
                )
                text = response.choices[0].message.content
                return json.loads(text)
            except Exception as e:
                print(f"Groq Fehler: {e}")
                return self._simuliere_antwort(spracheingabe)
        else:
            return self._simuliere_antwort(spracheingabe)
    
    def _simuliere_antwort(self, eingabe):
        eingabe = eingabe.lower()
        
        if "vorwärts" in eingabe or "vor" in eingabe:
            return {"befehl": "vorwaerts", "geschwindigkeit": 60, "dauer": 2, "begruendung": "Na gut, ich fahr vorwärts!"}
        elif "stopp" in eingabe or "stop" in eingabe or "halt" in eingabe:
            return {"befehl": "stop", "geschwindigkeit": 0, "dauer": 0, "begruendung": "Endlich Pause!"}
        elif "links" in eingabe:
            return {"befehl": "links", "geschwindigkeit": 40, "dauer": 1, "begruendung": "Links also..."}
        elif "rechts" in eingabe:
            return {"befehl": "rechts", "geschwindigkeit": 40, "dauer": 1, "begruendung": "Rechts, klar!"}
        elif "rückwärts" in eingabe or "zurück" in eingabe:
            return {"befehl": "rueckwaerts", "geschwindigkeit": 40, "dauer": 2, "begruendung": "Rückwärts? Wirklich?"}
        else:
            return {"befehl": "stop", "geschwindigkeit": 0, "dauer": 0, "begruendung": "Was meinst du damit?"}
    
    def fahren(self, kommando):
        befehl = kommando.get("befehl")
        geschwindigkeit = kommando.get("geschwindigkeit", 50)
        begruendung = kommando.get("begruendung", "")
        
        print(f"🤖 Bruno: {begruendung}")
        
        if befehl == "vorwaerts":
            self.auto.vorwaerts(geschwindigkeit)
        elif befehl == "rueckwaerts":
            self.auto.rueckwaerts(geschwindigkeit)
        elif befehl == "links":
            self.auto.links(geschwindigkeit)
        elif befehl == "rechts":
            self.auto.rechts(geschwindigkeit)
        elif befehl == "stop":
            self.auto.stop()
    
    def sprachbefehl(self, eingabe):
        kommando = self.befehl_interpretieren(eingabe)
        self.fahren(kommando)