from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from speech_listener import wakeup_word
import voice_talk
import ollama

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 

desiredModel='llama3.2:latest'

# Server is combining the two snippets from speech.py and voice_talk.py
# Python is only sending data to the mirror, so it's showing what is being said.
# TODO: Implement text from mirror.

@app.route('/sendData', methods=['GET'])
def send_data():
    user_input = request.args.get('message')
    response = ollama.chat(model=desiredModel, messages=[
    {
        'role': 'user',
        'content': user_input, 
    },
    ])

    OllamaResponse=response['message']['content']

    print("Answer: ", OllamaResponse)
    voice_talk.generate_voice(OllamaResponse)
    return jsonify({"text": f"{OllamaResponse}"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
    wakeup_word()
