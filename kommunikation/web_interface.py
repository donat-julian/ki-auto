# Web Interface für KI-RC-Auto
# Läuft auf dem Raspberry Pi
# Handy-Browser zeigt Kamera-Stream und ermöglicht Sprachsteuerung

from flask import Flask, render_template, Response, jsonify, request
from flask_socketio import SocketIO
import sys
import os
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kamera.kamera import Kamera
from motor.motor_steuerung import Auto
from sprachsteuerung.claude_steuerung import ClaudeSteuerung

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ki-auto-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Hardware initialisieren
auto = Auto()
kamera = Kamera()
claude = ClaudeSteuerung(auto=auto)

def kamera_stream():
    """
    Generiert kontinuierlichen Kamera-Stream
    """
    while True:
        try:
            import cv2
            frame = kamera.frame_holen()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if frame is not None:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.01)  # ~30 FPS
        except Exception as e:
            print(f"Stream Fehler: {e}")
            time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    """Kamera-Stream Route"""
    return Response(
        kamera_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/befehl', methods=['POST'])
def befehl():
    """Empfängt Sprachbefehle vom Handy"""
    daten = request.json
    eingabe = daten.get('text', '')
    
    print(f"🎤 Befehl empfangen: {eingabe}")
    kommando = claude.befehl_interpretieren(eingabe)
    claude.fahren(kommando)
    
    return jsonify({
        'status': 'ok',
        'befehl': kommando.get('befehl'),
        'antwort': kommando.get('begruendung')
    })

@app.route('/manuell', methods=['POST'])
def manuell():
    """Manuelle Steuerung vom Handy"""
    daten = request.json
    richtung = daten.get('richtung', 'stop')
    
    if richtung == 'vorwaerts':
        auto.vorwaerts()
    elif richtung == 'rueckwaerts':
        auto.rueckwaerts()
    elif richtung == 'links':
        auto.links()
    elif richtung == 'rechts':
        auto.rechts()
    elif richtung == 'stop':
        auto.stop()
    
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("🌐 Web Interface startet...")
    print("📱 Öffne http://ki-auto.local:5000 auf deinem Handy!")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)