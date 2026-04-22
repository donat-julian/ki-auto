# Kamera für KI-RC-Auto
# Verwendet Raspberry Pi Camera Module 3
# Unterstützt Simulation (PC) und echte Hardware (Pi)

import os
import time

try:
    from picamera2 import Picamera2
    SIMULATION = False
    print("📷 Kamera-Modus: Echter Raspberry Pi")
except ImportError:
    SIMULATION = True
    print("💻 Kamera-Modus: Simulation")


class Kamera:
    """
    Klasse für die Raspberry Pi Kamera
    Macht Fotos und Videos für KI-Verarbeitung
    """
    
    def __init__(self):
        if not SIMULATION:
            self.kamera = Picamera2()
            config = self.kamera.create_still_configuration(
                main={"size": (1280, 720)}
                self.kamera.set_controls({"Rotation": 180})
            )
            self.kamera.configure(config)
            self.kamera.start()
            time.sleep(1)  # Kamera aufwärmen
            print("✅ Kamera initialisiert (640x480)")
        else:
            print("✅ Kamera simuliert")
    
    def foto_machen(self, pfad="~/foto.jpg"):
        """
        Macht ein Foto und speichert es
        """
        pfad = os.path.expanduser(pfad)
        
        if not SIMULATION:
            self.kamera.capture_file(pfad)
            print(f"📸 Foto gespeichert: {pfad}")
        else:
            print(f"📸 Simulation: Foto würde gespeichert als {pfad}")
        
        return pfad
    
    def frame_holen(self):
        """
        Holt einen einzelnen Frame als Array
        Wird später für YOLOv8 verwendet
        """
        if not SIMULATION:
            frame = self.kamera.capture_array()
            return frame
        else:
            print("💻 Simulation: Leerer Frame")
            return None
    
    def stoppen(self):
        """
        Kamera sauber beenden
        """
        if not SIMULATION:
            self.kamera.stop()
            print("Kamera gestoppt")


# Test
if __name__ == "__main__":
    kamera = Kamera()
    kamera.foto_machen("~/test_ki_auto.jpg")
    time.sleep(1)
    kamera.stoppen()