from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import serial
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///soil_moisture.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    moisture_value = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, moisture_value):
        self.moisture_value = moisture_value

# Function to read data from serial port
def read_serial_data():
    try:
        with serial.Serial('COM8', 9600, timeout=2) as arduino:  # Adjust the timeout as needed
            time.sleep(2)  # Wait for the serial connection to initialize
            if arduino.in_waiting > 0:
                sensor_value = arduino.readline().decode().strip()
                print(f"Sensor value read: {sensor_value}")  # Log the sensor value for debugging
                try:
                    moisture_value = int(sensor_value)
                except ValueError:
                    print("Failed to convert sensor value to int.")
                    moisture_value = 0
                return moisture_value
            else:
                print("No data waiting in serial buffer.")
                return None
    except serial.SerialException as e:
        print(f"Failed to establish serial connection: {e}")
        return None

@app.route('/')
def index():
    moisture_value = read_serial_data()

    if moisture_value is not None:
        if moisture_value < 200:
            moisture_status = "I Am Dead ☠"
        elif moisture_value < 500:
            moisture_status = "I Am Happy 😇"
        else:
            moisture_status = "I Am Sad 😢"

        reading = Reading(moisture_value)
        db.session.add(reading)
        db.session.commit()
    else:
        moisture_value = 0
        moisture_status = "Serial connection error"

    return render_template('index.html', status=moisture_status, moisture_value=moisture_value)

@app.route('/readings')
def readings():
    readings = Reading.query.all()
    return render_template('readings.html', readings=readings)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and table are created
    app.run(debug=True)
