# Motorsteuerung für KI-RC-Auto
# Simuliert die Motorsteuerung des Raspberry Pi
# Später werden die GPIO-Pins des Pi angesprochen

class Motor:
    """
    Klasse für die Motorsteuerung
    Simuliert einen einzelnen Motor
    """
    
    def __init__(self, name):
        # name = Name des Motors (z.B. "Vorne Links")
        self.name = name
        self.geschwindigkeit = 0  # 0 = stop, 100 = volle Kraft
        self.richtung = "stop"
    
    def vorwaerts(self, geschwindigkeit=50):
        self.richtung = "vorwaerts"
        self.geschwindigkeit = geschwindigkeit
        print(f"{self.name}: Vorwärts mit {geschwindigkeit}% Geschwindigkeit")
    
    def rueckwaerts(self, geschwindigkeit=50):
        self.richtung = "rueckwaerts"
        self.geschwindigkeit = geschwindigkeit
        print(f"{self.name}: Rückwärts mit {geschwindigkeit}% Geschwindigkeit")
    
    def stop(self):
        self.richtung = "stop"
        self.geschwindigkeit = 0
        print(f"{self.name}: Gestoppt")


class Auto:
    """
    Klasse für das gesamte Fahrzeug
    Steuert alle 4 Motoren gleichzeitig
    """
    
    def __init__(self):
        # 4 Motoren für 4WD
        self.motor_vl = Motor("Vorne Links")
        self.motor_vr = Motor("Vorne Rechts")
        self.motor_hl = Motor("Hinten Links")
        self.motor_hr = Motor("Hinten Rechts")
    
    def vorwaerts(self, geschwindigkeit=50):
        print("\n--- Auto fährt VORWÄRTS ---")
        self.motor_vl.vorwaerts(geschwindigkeit)
        self.motor_vr.vorwaerts(geschwindigkeit)
        self.motor_hl.vorwaerts(geschwindigkeit)
        self.motor_hr.vorwaerts(geschwindigkeit)
    
    def rueckwaerts(self, geschwindigkeit=50):
        print("\n--- Auto fährt RÜCKWÄRTS ---")
        self.motor_vl.rueckwaerts(geschwindigkeit)
        self.motor_vr.rueckwaerts(geschwindigkeit)
        self.motor_hl.rueckwaerts(geschwindigkeit)
        self.motor_hr.rueckwaerts(geschwindigkeit)
    
    def links(self, geschwindigkeit=50):
        print("\n--- Auto fährt LINKS ---")
        self.motor_vl.rueckwaerts(geschwindigkeit)
        self.motor_hl.rueckwaerts(geschwindigkeit)
        self.motor_vr.vorwaerts(geschwindigkeit)
        self.motor_hr.vorwaerts(geschwindigkeit)
    
    def rechts(self, geschwindigkeit=50):
        print("\n--- Auto fährt RECHTS ---")
        self.motor_vl.vorwaerts(geschwindigkeit)
        self.motor_hl.vorwaerts(geschwindigkeit)
        self.motor_vr.rueckwaerts(geschwindigkeit)
        self.motor_hr.rueckwaerts(geschwindigkeit)
    
    def stop(self):
        print("\n--- Auto STOPPT ---")
        self.motor_vl.stop()
        self.motor_vr.stop()
        self.motor_hl.stop()
        self.motor_hr.stop()


# Test - simuliert eine kleine Fahrt
if __name__ == "__main__":
    auto = Auto()
    
    auto.vorwaerts(75)
    auto.links(50)
    auto.rechts(50)
    auto.rueckwaerts(30)
    auto.stop()