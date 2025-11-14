from machine import Pin, PWM
import time
import network
import urequests

# ===== WIFI CONFIGURATION =====
SSID = "Lab Telkom"
PASSWORD = ""
FLASK_SERVER = "http://172.16.14.169:5001"

# ===== SENSOR & BUZZER SETUP =====
trig = Pin(13, Pin.OUT)
echo = Pin(12, Pin.IN)
buzzer = PWM(Pin(14))
JARAK_AMAN = 50

# ===== VARIABLES FOR NON-BLOCKING =====
last_send_time = 0
send_interval = 2  # Kirim data setiap 2 detik
wifi_connected = False


def connect_wifi():
    global wifi_connected
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to WiFi...")
    for i in range(15):
        if wlan.isconnected():
            print(f"✅ WiFi Connected! IP: {wlan.ifconfig()[0]}")
            wifi_connected = True
            return True
        time.sleep(1)
    print("❌ WiFi connection failed")
    wifi_connected = False
    return False


def baca_jarak():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    while echo.value() == 0:
        signal_off = time.ticks_us()
    while echo.value() == 1:
        signal_on = time.ticks_us()

    time_passed = signal_on - signal_off
    jarak = (time_passed * 0.0343) / 2
    return jarak


def bunyikan_buzzer(jarak):
    # BUZZER INSTANT - TANPA TUNGGU WiFi!
    if jarak < JARAK_AMAN:
        buzzer.freq(1000)
        buzzer.duty(512)
        return "VISITOR_DETECTED"
    else:
        buzzer.duty(0)
        return "AREA_CLEAR"


def kirim_ke_flask(jarak, status):
    try:
        data = {
            "distance": round(jarak, 1),
            "status": status,
            "timestamp": time.time()
        }

        # Timeout sangat singkat, jangan blocking lama
        response = urequests.post(f"{FLASK_SERVER}/api/sensor", json=data, timeout=1)
        print(f"📤 Data terkirim: {jarak:.1f}cm")
        response.close()
    except Exception as e:
        print(f"❌ Gagal kirim: {e}")


# ===== MAIN PROGRAM =====
print("🚀 SMART VISITOR DETECTOR - OPTIMIZED")
connect_wifi()

print(f"Buzzer akan menyala INSTANT jika objek < {JARAK_AMAN}cm")
print("Data dikirim ke Flask setiap 2 detik (non-blocking)")

try:
    while True:
        # Baca sensor - PRIORITAS UTAMA
        jarak = baca_jarak()

        # BUZZER INSTANT - tidak tunggu apapun!
        status = bunyikan_buzzer(jarak)

        # Tampilkan di serial
        if status == "VISITOR_DETECTED":
            print(f"🚨 TAMU! Jarak: {jarak:.1f}cm - BUZZER: INSTANT")
        else:
            print(f"✅ AMAN. Jarak: {jarak:.1f}cm")

        # Kirim ke Flask HANYA jika waktu interval sudah cukup
        current_time = time.time()
        if wifi_connected and (current_time - last_send_time) >= send_interval:
            kirim_ke_flask(jarak, status)
            last_send_time = current_time

        time.sleep(0.1)  # Loop cepat untuk respons sensor instant

except KeyboardInterrupt:
    buzzer.duty(0)
    print("\n🛑 Program dihentikan")
