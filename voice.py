# 2️⃣ Build the model and load the default voicepack
from kokoro import generate
from IPython.display import display, Audio
from models import build_model
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu' # Let it run on the GPU if available
MODEL = build_model('kokoro-v0_19.pth', device)
VOICE_NAME = [
    'af', # Default voice is a 50-50 mix of Bella & Sarah
    'af_bella', 'af_sarah', 'am_adam', 'am_michael',
    'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
    'af_nicole', 'af_sky',
][6]
VOICEPACK = torch.load(f'voices/{VOICE_NAME}.pt', weights_only=True).to(device)
print(f'Loaded voice: {VOICE_NAME}')

def generate_voice(text):
    audio, out_ps = generate(MODEL, text, VOICEPACK, lang=VOICE_NAME[0])
    display(Audio(data=audio, rate=24000, autoplay=True))
    print(out_ps)

generate_voice(text="You look awesome today!")
