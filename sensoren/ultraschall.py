# Ultraschallsensor HC-SR04
# Misst die Entfernung zu Hindernissen
# Auf dem Raspberry Pi werden echte GPIO-Pins verwendet
# Hier simulieren wir den Sensor

import random
import time

class Ultraschall:
    """
    Klasse für den Ultraschallsensor HC-SR04
    Sendet Schallwellen aus und misst wie lange sie zurückbrauchen
    Daraus berechnet man die Entfernung
    """
    
    def __init__(self, position="vorne"):
        # position = wo ist der Sensor am Auto
        self.position = position
        print(f"Ultraschallsensor {position} initialisiert")
    
    def entfernung_messen(self):
        """
        Misst die Entfernung in cm
        Auf dem echten Pi: GPIO-Signal senden und Zeit messen
        Hier: zufällige Simulation
        """
        # Simulation: zufällige Entfernung zwischen 5 und 200 cm
        entfernung = random.uniform(5, 200)
        return round(entfernung, 1)
    
    def ist_hindernis(self, mindestabstand=30):
        """
        Gibt True zurück wenn ein Hindernis näher als mindestabstand cm ist
        Standard: 30cm Sicherheitsabstand
        """
        entfernung = self.entfernung_messen()
        print(f"Sensor {self.position}: {entfernung} cm")
        
        if entfernung < mindestabstand:
            print(f"⚠️  HINDERNIS ERKANNT! Nur {entfernung} cm Abstand!")
            return True
        return False


class HindernisSystem:
    """
    Verwaltet alle Ultraschallsensoren am Auto
    """
    
    def __init__(self):
        self.sensor_vorne = Ultraschall("vorne")
        self.sensor_links = Ultraschall("links")
        self.sensor_rechts = Ultraschall("rechts")
    
    def alle_sensoren_pruefen(self):
        """
        Prüft alle Sensoren gleichzeitig
        Gibt zurück wo Hindernisse sind
        """
        print("\n--- Sensoren prüfen ---")
        hindernisse = {
            "vorne": self.sensor_vorne.ist_hindernis(),
            "links": self.sensor_links.ist_hindernis(),
            "rechts": self.sensor_rechts.ist_hindernis()
        }
        return hindernisse
    
    def sicherer_weg(self):
        """
        Findet die sicherste Fahrtrichtung
        """
        hindernisse = self.alle_sensoren_pruefen()
        
        if not hindernisse["vorne"]:
            return "vorwaerts"
        elif not hindernisse["rechts"]:
            return "rechts"
        elif not hindernisse["links"]:
            return "links"
        else:
            return "rueckwaerts"


# Test
if __name__ == "__main__":
    system = HindernisSystem()
    
    for i in range(3):
        print(f"\n=== Messung {i+1} ===")
        weg = system.sicherer_weg()
        print(f"Empfohlene Richtung: {weg}")
        time.sleep(1)