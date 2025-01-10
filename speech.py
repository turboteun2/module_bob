from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import voice_talk

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 

received_text = "" 
# Server is combining the two snippets from speech.py and voice_talk.py
# Python is only sending data to the mirror, so it's showing what is being said.
# TODO: Implement text from mirror.

@app.route('/add', methods=['POST']) # For testing
def send():
    global received_text
    data = request.json
    received_text = data.get("text", "")
    
    socketio.emit('update_text', {"text": received_text})
    voice_talk.generate_voice(received_text)
    return jsonify({"text": "Text received!"})

@app.route('/sendData', methods=['POST']) # For testing
def send_data():
    
    answer_llama = "I am a llama, I don't know"
    return jsonify({"text": f"{answer_llama}"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
