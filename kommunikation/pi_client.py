# pi_client.py - läuft auf dem Raspberry Pi
# Sendet Sensordaten an den PC
# Empfängt Fahrkommandos und führt sie aus

import asyncio
import websockets
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor.motor_steuerung import Auto
from sensoren.ultraschall import HindernisSystem

class PiClient:
    """
    WebSocket Client auf dem Raspberry Pi
    - Liest Sensoren aus
    - Sendet Daten an PC
    - Empfängt und führt Fahrkommandos aus
    """
    
    def __init__(self, server_ip="192.168.2.100", port=8765):
        # server_ip = IP des PCs im Heimnetzwerk
        self.server_url = f"ws://{server_ip}:{port}"
        self.auto = Auto()
        self.sensoren = HindernisSystem()
        print(f"🤖 Pi-Client bereit, verbinde mit {self.server_url}")
    
    def fahren(self, kommando):
        """
        Führt empfangenes Fahrkommando aus
        """
        befehl = kommando.get("befehl")
        geschwindigkeit = kommando.get("geschwindigkeit", 50)
        
        print(f"⚙️  Führe aus: {befehl} mit {geschwindigkeit}%")
        
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
    
    async def verbinden(self):
        """
        Verbindet mit dem PC-Server und sendet Sensordaten
        """
        async with websockets.connect(self.server_url) as websocket:
            print("✅ Mit PC verbunden!")
            
            while True:
                # Sensoren auslesen
                hindernisse = self.sensoren.alle_sensoren_pruefen()
                
                # Daten an PC senden
                nachricht = json.dumps({
                    "typ": "sensoren",
                    "hindernisse": hindernisse
                })
                
                await websocket.send(nachricht)
                
                # Fahrkommando vom PC empfangen
                antwort = await websocket.recv()
                kommando = json.loads(antwort)
                
                # Kommando ausführen
                self.fahren(kommando)
                
                await asyncio.sleep(0.5)


# Test
if __name__ == "__main__":
    # server_ip = IP deines PCs
    client = PiClient(server_ip="127.0.0.1")
    asyncio.run(client.verbinden())