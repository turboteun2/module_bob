import torch
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr
from datasets import load_dataset
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

def stt():
    # Start listening to the user
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3-turbo"

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

    result = pipe(audio_log)
    print(result["text"])

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

microphone_index = input("Enter the index of the microphone you want to use: ")

def wakeup_word():
    r = sr.Recognizer()
    with sr.Microphone(device_index=int(microphone_index)) as source:
        print("Wake up Jarvis!")
        audio = r.listen(source)
        try:
            Jarvis_wake_word = r.recognize_google(audio, language="en-US")
            print(f"{Jarvis_wake_word}")
            if Jarvis_wake_word.lower() == "jarvis":
                print("Jarvis detected. You can now talk!")
                # Create audiolog for what the person is saying, when the user stops talking call stt.
                data, samplerate = sf.read("voices/start.wav")
                sd.play(data, samplerate)
                sd.wait() 
                # audio_log = r.listen(source)
                stt()
        except sr.UnknownValueError:
            print("I couldn't understand what you said.")
        except sr.RequestError as e:
            print(f"Google Speech Recognition service returned: {e}")

wakeup_word()