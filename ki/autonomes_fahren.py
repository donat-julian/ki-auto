# Autonomes Fahren
# Kombiniert Motorsteuerung und Ultraschallsensoren
# Das Auto fährt selbstständig und weicht Hindernissen aus

import sys
import os
import time

# Eigene Module importieren
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor.motor_steuerung import Auto
from sensoren.ultraschall import HindernisSystem

class AutonomesFahren:
    """
    Hauptklasse für autonomes Fahren
    Verbindet Sensoren mit Motorsteuerung
    """
    
    def __init__(self):
        self.auto = Auto()
        self.sensoren = HindernisSystem()
        self.fahrt_aktiv = False
        print("\n🚗 KI-Auto initialisiert!")
    
    def entscheidung_treffen(self):
        """
        Liest Sensoren aus und entscheidet was zu tun ist
        """
        weg = self.sensoren.sicherer_weg()
        
        if weg == "vorwaerts":
            self.auto.vorwaerts(60)
        elif weg == "rechts":
            print("Hindernis vorne - weiche nach rechts aus!")
            self.auto.rechts(40)
            time.sleep(0.5)
        elif weg == "links":
            print("Hindernis vorne und rechts - weiche nach links aus!")
            self.auto.links(40)
            time.sleep(0.5)
        else:
            print("Überall Hindernisse - fahre zurück!")
            self.auto.rueckwaerts(30)
            time.sleep(1)
    
    def starten(self, dauer=10):
        """
        Startet autonomes Fahren für eine bestimmte Dauer
        dauer = Sekunden
        """
        print(f"\n🚀 Autonomes Fahren startet für {dauer} Sekunden!")
        self.fahrt_aktiv = True
        
        start = time.time()
        
        while time.time() - start < dauer:
            self.entscheidung_treffen()
            time.sleep(0.5)
        
        self.auto.stop()
        print("\n✅ Autonomes Fahren beendet!")


# Test
if __name__ == "__main__":
    fahrzeug = AutonomesFahren()
    fahrzeug.starten(dauer=5)