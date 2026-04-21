# Motorsteuerung für KI-RC-Auto
# Unterstützt Simulation (PC/Test) und echte Hardware (Raspberry Pi)

try:
    import RPi.GPIO as GPIO
    SIMULATION = False
    print("🔧 GPIO-Modus: Echter Raspberry Pi")
except ImportError:
    SIMULATION = True
    print("💻 GPIO-Modus: Simulation")

# GPIO-Pins für L298N Motortreiber
# Linke Motoren
IN1 = 17  # Vorwärts links
IN2 = 18  # Rückwärts links
ENA = 12  # Geschwindigkeit links (PWM)

# Rechte Motoren
IN3 = 27  # Vorwärts rechts
IN4 = 22  # Rückwärts rechts
ENB = 13  # Geschwindigkeit rechts (PWM)

class Motor:
    def __init__(self, name):
        self.name = name
        self.geschwindigkeit = 0
        self.richtung = "stop"

    def vorwaerts(self, geschwindigkeit=50):
        self.richtung = "vorwaerts"
        self.geschwindigkeit = geschwindigkeit
        print(f"{self.name}: Vorwärts mit {geschwindigkeit}%")

    def rueckwaerts(self, geschwindigkeit=50):
        self.richtung = "rueckwaerts"
        self.geschwindigkeit = geschwindigkeit
        print(f"{self.name}: Rückwärts mit {geschwindigkeit}%")

    def stop(self):
        self.richtung = "stop"
        self.geschwindigkeit = 0
        print(f"{self.name}: Gestoppt")


class Auto:
    def __init__(self):
        self.motor_links = Motor("Links")
        self.motor_rechts = Motor("Rechts")
        
        if not SIMULATION:
            self._gpio_setup()
    
    def _gpio_setup(self):
        """Initialisiert GPIO-Pins für L298N"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        pins = [IN1, IN2, IN3, IN4, ENA, ENB]
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
        
        # PWM für Geschwindigkeitssteuerung
        self.pwm_links = GPIO.PWM(ENA, 1000)
        self.pwm_rechts = GPIO.PWM(ENB, 1000)
        self.pwm_links.start(0)
        self.pwm_rechts.start(0)
        print("✅ GPIO initialisiert")
    
    def _gpio_fahren(self, links_vor, links_rueck, rechts_vor, rechts_rueck, geschwindigkeit):
        """Steuert GPIO-Pins direkt"""
        if SIMULATION:
            return
        GPIO.output(IN1, links_vor)
        GPIO.output(IN2, links_rueck)
        GPIO.output(IN3, rechts_vor)
        GPIO.output(IN4, rechts_rueck)
        self.pwm_links.ChangeDutyCycle(geschwindigkeit)
        self.pwm_rechts.ChangeDutyCycle(geschwindigkeit)

    def vorwaerts(self, geschwindigkeit=50):
        print("\n--- Auto fährt VORWÄRTS ---")
        self.motor_links.vorwaerts(geschwindigkeit)
        self.motor_rechts.vorwaerts(geschwindigkeit)
        self._gpio_fahren(True, False, True, False, geschwindigkeit)

    def rueckwaerts(self, geschwindigkeit=50):
        print("\n--- Auto fährt RÜCKWÄRTS ---")
        self.motor_links.rueckwaerts(geschwindigkeit)
        self.motor_rechts.rueckwaerts(geschwindigkeit)
        self._gpio_fahren(False, True, False, True, geschwindigkeit)

    def links(self, geschwindigkeit=50):
        print("\n--- Auto fährt LINKS ---")
        self.motor_links.rueckwaerts(geschwindigkeit)
        self.motor_rechts.vorwaerts(geschwindigkeit)
        self._gpio_fahren(False, True, True, False, geschwindigkeit)

    def rechts(self, geschwindigkeit=50):
        print("\n--- Auto fährt RECHTS ---")
        self.motor_links.vorwaerts(geschwindigkeit)
        self.motor_rechts.rueckwaerts(geschwindigkeit)
        self._gpio_fahren(True, False, False, True, geschwindigkeit)

    def stop(self):
        print("\n--- Auto STOPPT ---")
        self.motor_links.stop()
        self.motor_rechts.stop()
        self._gpio_fahren(False, False, False, False, 0)
    
    def cleanup(self):
        """GPIO aufräumen beim Beenden"""
        if not SIMULATION:
            self.stop()
            GPIO.cleanup()
            print("GPIO cleanup durchgeführt")


if __name__ == "__main__":
    auto = Auto()
    auto.vorwaerts(75)
    auto.links(50)
    auto.rechts(50)
    auto.rueckwaerts(30)
    auto.stop()
    auto.cleanup()