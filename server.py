from flask import Flask, request, jsonify
import threading
from flask_socketio import SocketIO
from speech_listener import wakeup_word
import voice_talk
import ollama

app = Flask(__name__)
socketio = SocketIO(app)

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

def sendData(question):
    # user_input = request.args.get('message')
    response = ollama.chat(model=desiredModel, messages=[
    {
        'role': 'user',
        'content': question, 
    },
    ])

    OllamaResponse=response['message']['content']

    print("Answer: ", OllamaResponse)
    voice_talk.generate_voice(OllamaResponse)

def run_py():
    while True:
        result = input("How can I assist you sir? ") # wakeup_word()
        if result: sendData(result)
    

if __name__ == "__main__":
    server_thread = threading.Thread(target=lambda: socketio.run(app, host="0.0.0.0", port=5001))
    server_thread.daemon = True
    server_thread.start()

    run_py()