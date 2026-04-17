# server.py - läuft auf dem PC
# Empfängt Kamerabild und Sensordaten vom Raspberry Pi
# Verarbeitet KI (YOLOv8, Claude) und sendet Fahrkommandos zurück

import asyncio
import websockets
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sprachsteuerung.claude_steuerung import ClaudeSteuerung

class KIServer:
    """
    WebSocket Server auf dem PC
    - Empfängt Sensordaten vom Pi
    - Verarbeitet KI-Logik
    - Sendet Fahrkommandos zurück
    """
    
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.claude = ClaudeSteuerung()
        print(f"🖥️  KI-Server bereit auf {host}:{port}")
    
    async def verarbeite_nachricht(self, nachricht):
        """
        Verarbeitet eingehende Nachrichten vom Pi
        """
        daten = json.loads(nachricht)
        typ = daten.get("typ")
        
        if typ == "sensoren":
            # Sensordaten vom Pi - Entscheidung treffen
            hindernisse = daten.get("hindernisse", {})
            return self.entscheidung_hindernisse(hindernisse)
        
        elif typ == "sprachbefehl":
            # Sprachbefehl - Claude API fragen
            eingabe = daten.get("eingabe", "")
            kommando = self.claude.befehl_interpretieren(eingabe)
            return kommando
        
        else:
            return {"befehl": "stop", "begruendung": "Unbekannter Nachrichtentyp"}
    
    def entscheidung_hindernisse(self, hindernisse):
        """
        Entscheidet Fahrtrichtung basierend auf Sensordaten
        """
        if not hindernisse.get("vorne"):
            return {"befehl": "vorwaerts", "geschwindigkeit": 60}
        elif not hindernisse.get("rechts"):
            return {"befehl": "rechts", "geschwindigkeit": 40}
        elif not hindernisse.get("links"):
            return {"befehl": "links", "geschwindigkeit": 40}
        else:
            return {"befehl": "rueckwaerts", "geschwindigkeit": 30}
    
    async def verbindung_handler(self, websocket):
        """
        Verwaltet eingehende WebSocket-Verbindungen
        """
        print(f"🔌 Raspberry Pi verbunden!")
        
        try:
            async for nachricht in websocket:
                print(f"📨 Empfangen: {nachricht}")
                antwort = await self.verarbeite_nachricht(nachricht)
                await websocket.send(json.dumps(antwort))
                print(f"📤 Gesendet: {antwort}")
        
        except websockets.exceptions.ConnectionClosed:
            print("❌ Verbindung getrennt")
    
    async def starten(self):
        """
        Startet den WebSocket Server
        """
        async with websockets.serve(self.verbindung_handler, self.host, self.port):
            print(f"✅ Server läuft auf ws://{self.host}:{self.port}")
            print("Warte auf Verbindung vom Raspberry Pi...")
            await asyncio.Future()


# Test
if __name__ == "__main__":
    server = KIServer()
    asyncio.run(server.starten())