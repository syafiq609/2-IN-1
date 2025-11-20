# 🚪 Sistem Deteksi Tamu Otomatis - IoT Project

**Real-time Visitor Detection System dengan ESP32 & Flask Dashboard**

## 📖 Tentang Project
Sistem IoT untuk mendeteksi tamu secara otomatis menggunakan sensor ultrasonik dan menampilkan status real-time pada dashboard web.

## 🎯 Fitur Utama
- ✅ **Deteksi Real-time** - Sensor HC-SR04 mendeteksi tamu
- ✅ **Notifikasi Buzzer** - Bunyi saat ada tamu
- ✅ **Dashboard Web** - Monitoring real-time dengan UI modern
- ✅ **Bahasa Indonesia** - Status "ADA TAMU!" dan "TENANG"
- ✅ **Auto-Refresh** - Update otomatis setiap detik

## 🔌 Komponen Hardware
- ESP32 Development Board
- Sensor Ultrasonik HC-SR04
- Buzzer
- Breadboard & Kabel Jumper

## 💻 Teknologi Software
- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **IoT**: MicroPython pada ESP32
- **Version Control**: Git & GitHub

## 🚀 Cara Menjalankan
1. **Hardware**: Hubungkan ESP32 + Sensor + Buzzer
2. **ESP32**: Upload kode `esp32/visitor_detector.py`
3. **Flask**: Jalankan `python app.py`
4. **Akses**: Buka `http://localhost:5001`

## 📁 Struktur Project
2-IN-1/
├── app.py # Flask server
├── requirements.txt # Dependencies
├── templates/
│ └── index.html # Website dashboard
├── esp32/
│ └── visitor_detector.py # Kode ESP32
└── README.md # Dokumentasi

## 👥 Developer
**Syafiq** - Siswa SMK - IoT & Web Development
**meylani** - Siswa SMK - hadware 
---
*Project Tugas Sekolah - Integrasi Sistem IoT*
