from flask import Flask, render_template, request, jsonify
import json
import time

app = Flask(__name__)

# Simpan data terakhir - SESUAIKAN DENGAN WEBSITE BAHASA INDONESIA
last_sensor_data = {
    'distance': 0,
    'status': 'TENANG',  # ← UBAH: 'AREA_CLEAR' → 'TENANG'
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

    # Konversi status dari ESP32 ke bahasa Indonesia untuk website
    status_indonesia = 'TENANG'  # default
    if data['status'] == 'VISITOR_DETECTED':
        status_indonesia = 'ADA TAMU'
    elif data['status'] == 'AREA_CLEAR':
        status_indonesia = 'TENANG'

    last_sensor_data = {
        'distance': data['distance'],
        'status': status_indonesia,  # ← PAKAI STATUS BAHASA INDONESIA
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