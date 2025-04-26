from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/save_line', methods=['POST'])
def save_line():
    data = request.get_json()
    print('Received line points:', data)
    return jsonify({'status': "success", "message": 'Line received!'})
