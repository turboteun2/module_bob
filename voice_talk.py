from transformers import pipeline
from datasets import load_dataset
import sounddevice as sd
import soundfile as sf
import torch
import os

synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

def del_voice(file_path):
    # Function to delete the last voice prompt, saves memory
    if os.path.exists(file_path):
        os.remove(file_path)

def generate_voice(text):
    file_path = "last_prompt.wav"
    del_voice(file_path)

    speech = synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})
    sf.write(file_path, speech["audio"], samplerate=speech["sampling_rate"])
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()  # Wait until the audio is played completely

    del_voice(file_path)

generate_voice(text=input())
