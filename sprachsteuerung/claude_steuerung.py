# Sprachsteuerung via Claude API
# Das Auto versteht natürliche Sprachbefehle
# Claude interpretiert die Befehle und gibt Fahrkommandos zurück

import sys
import os
import json
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor.motor_steuerung import Auto

class ClaudeSteuerung:
    """
    Verbindet Claude API mit der Motorsteuerung
    Claude versteht natürliche Sprache und gibt Fahrkommandos zurück
    """
    
    def __init__(self, auto=None):
    if auto is None:
        self.auto = Auto()
    else:
        self.auto = auto
    self.api_url = "https://api.anthropic.com/v1/messages"
    # API Key - später aus Umgebungsvariable laden
    self.api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    
    self.system_prompt = """Du bist die KI-Steuerung eines RC-Autos.
    Der Benutzer gibt dir Fahrbefehle in natürlicher Sprache.
    Du antwortest NUR mit einem JSON-Objekt in diesem Format:
    {
        "befehl": "vorwaerts/rueckwaerts/links/rechts/stop",
        "geschwindigkeit": 0-100,
        "dauer": Sekunden,
        "begruendung": "kurze Erklärung"
    }
    Antworte IMMER nur mit dem JSON, nichts anderes."""
    
    def befehl_interpretieren(self, spracheingabe):
        """
        Sendet Spracheingabe an Claude und bekommt Fahrkommando zurück
        """
        print(f"\n🎤 Eingabe: {spracheingabe}")
        
        if not self.api_key:
            print("⚠️  Kein API Key - simuliere Antwort")
            return self._simuliere_antwort(spracheingabe)
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 200,
            "system": self.system_prompt,
            "messages": [
                {"role": "user", "content": spracheingabe}
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            antwort = response.json()
            text = antwort["content"][0]["text"]
            return json.loads(text)
        except Exception as e:
            print(f"API Fehler: {e}")
            return self._simuliere_antwort(spracheingabe)
    
    def _simuliere_antwort(self, eingabe):
        """
        Simuliert Claude-Antwort ohne API Key
        Für Tests und Entwicklung
        """
        eingabe = eingabe.lower()
        
        if "vorwärts" in eingabe or "vor" in eingabe:
            return {"befehl": "vorwaerts", "geschwindigkeit": 60, "dauer": 2, "begruendung": "Vorwärtsfahrt"}
        elif "stopp" in eingabe or "stop" in eingabe or "halt" in eingabe:
            return {"befehl": "stop", "geschwindigkeit": 0, "dauer": 0, "begruendung": "Anhalten"}
        elif "links" in eingabe:
            return {"befehl": "links", "geschwindigkeit": 40, "dauer": 1, "begruendung": "Links abbiegen"}
        elif "rechts" in eingabe:
            return {"befehl": "rechts", "geschwindigkeit": 40, "dauer": 1, "begruendung": "Rechts abbiegen"}
        elif "rückwärts" in eingabe or "zurück" in eingabe:
            return {"befehl": "rueckwaerts", "geschwindigkeit": 40, "dauer": 2, "begruendung": "Rückwärtsfahrt"}
        else:
            return {"befehl": "stop", "geschwindigkeit": 0, "dauer": 0, "begruendung": "Befehl nicht erkannt"}
    
    def fahren(self, kommando):
        """
        Führt das Fahrkommando aus
        """
        befehl = kommando.get("befehl")
        geschwindigkeit = kommando.get("geschwindigkeit", 50)
        begruendung = kommando.get("begruendung", "")
        
        print(f"🤖 Claude sagt: {begruendung}")
        print(f"⚙️  Befehl: {befehl} mit {geschwindigkeit}%")
        
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
        """
        Hauptfunktion - nimmt Spracheingabe und fährt
        """
        kommando = self.befehl_interpretieren(eingabe)
        self.fahren(kommando)


# Test
if __name__ == "__main__":
    steuerung = ClaudeSteuerung()
    
    befehle = [
        "Fahr vorwärts",
        "Biege links ab",
        "Fahr zurück",
        "Stopp!"
    ]
    
    for befehl in befehle:
        steuerung.sprachbefehl(befehl)
        print()