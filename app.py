from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Data simulasi sensor
    sensor_data = {
        'distance': 75,
        'status': 'ADA TAMU' if 75 < 100 else 'TENANG'
    }
    return render_template('index.html', data=sensor_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Pakai port 5001