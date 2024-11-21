from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

# Serve index.html
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/move-robot', methods=['POST'])
def move_robot():
    # Retrieve the list of selected items
    selected_items = request.json  # JSON data sent from the client

    if not selected_items:
        return jsonify({"message": "No items received"}), 400

    # Process the selected items (e.g., make the robot move)
    print("Selected items:", selected_items)

    # Simulate robot movement (replace this with your robot control code)
    for item in selected_items:
        print(f"Moving robot to pick up {item['name']}...")

    return jsonify({"message": "Robot is moving to designated areas!"})

# Serve static files (CSS, JS, etc.)
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


