from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 

received_text = "" 

@app.route('/send', methods=['POST'])
def send():
    global received_text
    data = request.json
    received_text = data.get("text", "")
    
    socketio.emit('update_text', {"text": received_text})
    
    return jsonify({"message": "Text received!"})

@app.route('/receive', methods=['GET'])
def receive():
    return jsonify({"text": received_text})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
