from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

saved_connections = []

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    print("Received data:", data)
    saved_connections.clear()
    saved_connections.extend(data)  # overwrite for simplicity
    return jsonify({"status": "success"})

@app.route('/connections', methods=['GET'])
def get_connections():
    return jsonify(saved_connections)

if __name__ == '__main__':
    app.run(debug=True)