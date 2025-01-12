import os
import torch
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3-turbo"
# Load Whisper model and processor
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

# List and select microphone
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone {index}: {name}")

microphone_index = int(input("Enter the index of the microphone you want to use: "))

def del_voice(file_path):
    # Function to delete the last voice prompt, saves memory
    if os.path.exists(file_path):
        os.remove(file_path)

def stt():
    recognizer = sr.Recognizer()
    file_path = "voices/input_text.wav"
    del_voice(file_path)
    
    with sr.Microphone(device_index=microphone_index) as source:
        data, samplerate = sf.read("voices/start.wav")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        sd.play(data, samplerate)
        sd.wait()

        audio_data = recognizer.listen(source, phrase_time_limit=10)
        audio_np = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16).astype(np.float32) / 32768.0
        sample_rate = audio_data.sample_rate

        sf.write(file_path, audio_np, sample_rate)
        result = pipe(file_path)
        
        print("Transcription:", result["text"])

        return result["text"]

def wakeup_word():
    r = sr.Recognizer()
    with sr.Microphone(device_index=int(microphone_index)) as source:
        audio = r.listen(source)
        try:
            Jarvis_wake_word = r.recognize_google(audio, language="en-US")
            if Jarvis_wake_word.lower() == "jarvis":
                print("Hello, sir")
                return stt()
        except sr.UnknownValueError:
            print("I couldn't understand what you said.")
        except sr.RequestError as e:
            print(f"Google Speech Recognition service returned: {e}")

# print(wakeup_word())