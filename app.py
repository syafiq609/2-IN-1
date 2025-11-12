from flask import Flask, render_template, request, jsonify
import json
import time

app = Flask(__name__)

# Simpan data terakhir - SESUAIKAN DENGAN ESP32
last_sensor_data = {
    'distance': 0,
    'status': 'AREA_CLEAR',  # ← GUNAKAN VALUE YANG SAMA DENGAN ESP32
    'timestamp': time.time()
}

@app.route('/')
def home():
    return render_template('index.html', data=last_sensor_data)

# API untuk terima data dari ESP32
@app.route('/api/sensor', methods=['POST'])
def receive_sensor_data():
    global last_sensor_data
    data = request.json
    last_sensor_data = {
        'distance': data['distance'],
        'status': data['status'],  # ← "VISITOR_DETECTED" atau "AREA_CLEAR"
        'timestamp': data['timestamp']
    }
    print(f"📡 Data diterima: {last_sensor_data}")
    return jsonify({'status': 'success'})

# API untuk website ambil data
@app.route('/api/status')
def get_status():
    return jsonify(last_sensor_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)