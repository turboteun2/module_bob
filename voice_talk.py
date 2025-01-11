from transformers import pipeline
from datasets import load_dataset
import sounddevice as sd
import soundfile as sf
import torch
import os
import re

synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

def del_voice(file_path):
    # Function to delete the last voice prompt, saves memory
    if os.path.exists(file_path):
        os.remove(file_path)

def split_text(text, max_tokens):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(' '.join(current_chunk)) >= max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def generate_voice(text, max_tokens=450):
    cleaned_text = re.sub(r'\s+', ' ', text.strip()) 
    text_chunks = split_text(cleaned_text, max_tokens)
    audio_files = []

    for i, chunk in enumerate(text_chunks):
        file_name = f"voices/speech_part_{i + 1}.wav"
        del_voice(file_name)
        speech = synthesiser(chunk, forward_params={"speaker_embeddings": speaker_embedding})
        sf.write(file_name, speech["audio"], samplerate=speech["sampling_rate"])
        audio_files.append(file_name)

    for file_name in audio_files:
        data, samplerate = sf.read(file_name)
        sd.play(data, samplerate)
        sd.wait() 

    for file_name in audio_files:
        os.remove(file_name)

# generate_voice(text="Listening...", max_tokens=450)