# main.py - Hauptprogramm KI-RC-Auto
# Verbindet alle Komponenten:
# - Motorsteuerung
# - Ultraschallsensoren
# - Autonomes Fahren
# - Sprachsteuerung via Claude

import sys
import time
from motor.motor_steuerung import Auto
from sensoren.ultraschall import HindernisSystem
from ki.autonomes_fahren import AutonomesFahren
from sprachsteuerung.claude_steuerung import ClaudeSteuerung

def menue():
    print("\n" + "="*40)
    print("    🚗 KI-RC-Auto Steuerung")
    print("="*40)
    print("1. Sprachsteuerung (Claude API)")
    print("2. Autonomes Fahren")
    print("3. Manuell fahren")
    print("4. Sensoren testen")
    print("5. Beenden")
    print("="*40)
    return input("Auswahl: ")

def manuell_fahren(auto):
    print("\nManuelle Steuerung:")
    print("w = vorwärts, s = rückwärts")
    print("a = links, d = rechts, x = stop, q = zurück")
    
    while True:
        taste = input("\nEingabe: ").lower()
        
        if taste == "w":
            auto.vorwaerts()
        elif taste == "s":
            auto.rueckwaerts()
        elif taste == "a":
            auto.links()
        elif taste == "d":
            auto.rechts()
        elif taste == "x":
            auto.stop()
        elif taste == "q":
            auto.stop()
            break

def main():
    print("🚗 KI-RC-Auto wird gestartet...")
    
    auto = Auto()
    sensoren = HindernisSystem()
    claude = ClaudeSteuerung()
    
    while True:
        auswahl = menue()
        
        if auswahl == "1":
            print("\n🎤 Sprachsteuerung aktiv (q zum Beenden)")
            while True:
                eingabe = input("Befehl: ")
                if eingabe.lower() == "q":
                    break
                claude.sprachbefehl(eingabe)
        
        elif auswahl == "2":
            fahrzeug = AutonomesFahren()
            fahrzeug.starten(dauer=10)
        
        elif auswahl == "3":
            manuell_fahren(auto)
        
        elif auswahl == "4":
            hindernisse = sensoren.alle_sensoren_pruefen()
            print(f"\nErgebnis: {hindernisse}")
        
        elif auswahl == "5":
            print("\n👋 Auf Wiedersehen!")
            auto.stop()
            break

if __name__ == "__main__":
    main()