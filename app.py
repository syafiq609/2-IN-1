from flask import Flask, render_template, request, jsonify
import json
import time
import os

app = Flask(__name__)

# Simpan data terakhir
last_sensor_data = {
    'distance': 0,
    'status': 'TENANG',
    'timestamp': time.time()
}

# ✅ TAMBAHIN: Health check untuk Railway
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': '2-IN-1 Visitor Detector'})

# ✅ TAMBAHIN: Catch-all route
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html', data=last_sensor_data)

# Route utama
@app.route('/')
def home():
    return render_template('index.html', data=last_sensor_data)

# API untuk terima data dari ESP32
@app.route('/api/sensor', methods=['POST'])
def receive_sensor_data():
    global last_sensor_data
    data = request.json

    status_indonesia = 'TENANG'
    if data['status'] == 'VISITOR_DETECTED':
        status_indonesia = 'ADA TAMU'
    elif data['status'] == 'AREA_CLEAR':
        status_indonesia = 'TENANG'

    last_sensor_data = {
        'distance': data['distance'],
        'status': status_indonesia,
        'timestamp': data['timestamp']
    }
    print(f"📡 Data diterima: {last_sensor_data}")
    return jsonify({'status': 'success'})

# API untuk website ambil data
@app.route('/api/status')
def get_status():
    return jsonify(last_sensor_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
