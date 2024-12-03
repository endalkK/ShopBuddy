from flask import Flask, request, jsonify, send_from_directory
import serial
import time
from barcode import read_barcode  # Ensure this is a function, not a top-level execution

app = Flask(__name__, static_folder='static')
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)  # Adjust port name as needed
time.sleep(2)  # Allow Arduino to reset

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/move-robot', methods=['POST'])
def move_robot():
    # Receive JSON data from the client
    selected_items = request.json

    if not selected_items:
        return jsonify({"message": "No items received"}), 400

    for item in selected_items:
        item_id = item.get("id")
        x, y = get_item_location(item_id)  # Get coordinates based on item ID
        if x is None or y is None:
            return jsonify({"message": f"Location for item ID {item_id} not found"}), 404

        # Send coordinates to Arduino
        send_coordinates_to_arduino(x, y)
        time.sleep(1)  # Allow Arduino to process

        # Wait for barcode scanning
        if not wait_for_barcode_scan():
            return jsonify({"message": f"Failed to read barcode for item ID {item_id}"}), 500

    return jsonify({"message": "Robot has successfully moved to all designated areas!"})

def get_item_location(item_id):
    """Map item IDs to (x, y) grid coordinates."""
    item_locations = {
        1: (3, 2),
        2: (6, 0),
        3: (8, 2),
    }
    return item_locations.get(item_id)

def send_coordinates_to_arduino(x, y):
    """Send goal coordinates to Arduino."""
    command = f"{x},{y}\n"
    print(f"Sending to Arduino: {command.strip()}")
    arduino.write(command.encode())  # Send as a string
    response = arduino.readline().decode().strip()  # Read Arduino's response
    print(f"Arduino response: {response}")

def wait_for_barcode_scan():
    """Wait for a successful barcode scan."""
    print("Waiting for barcode scan...")
    while True:
        if read_barcode():  
            print("Barcode successfully scanned!")
            return True
        time.sleep(1)  
        print("Retrying barcode scan...")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
