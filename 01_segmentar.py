import os
import sys
import torch
import numpy as np
import soundfile as sf
import argparse
from silero_vad import read_audio
from scipy.io.wavfile import write

# Parser d'arguments
parser = argparse.ArgumentParser(description="Segmenta àudio en fragments de veu.")
parser.add_argument("--input-wav", help="Fitxer d'àudio WAV d'entrada")
parser.add_argument("--output-dir", default="segments", help="Carpeta de sortida (opcional)")
args = parser.parse_args()

input_wav = args.input_wav
output_dir = args.output_dir

if not os.path.isfile(input_wav):
    print(f"Error: El fitxer d'àudio {input_wav} no existeix.")
    sys.exit(1)

os.makedirs(output_dir, exist_ok=True)

# Llegir àudio (assegura que és mono i a 16kHz)
audio = read_audio(input_wav, sampling_rate=16000)

print("Carrega del model de Silero VAD...")
model, utils = torch.hub.load('snakers4/silero-vad', 'silero_vad', force_reload=False)
(get_speech_timestamps, _, _, _, _) = utils

print("Detectant timestamps amb veu...")
speech_timestamps = get_speech_timestamps(audio, model, sampling_rate=16000)

# ignorar samples de menys de 1 segon
MIN_SAMPLES = int(1 * 16000)

print("Guardant segments...")
for i, t in enumerate(speech_timestamps):
    if (t['end'] - t['start']) < MIN_SAMPLES:
        continue  # Omet segments curts

    segment = audio[t['start']:t['end']]
    segment_np = segment.cpu().numpy()
    filename = os.path.join(output_dir, f"{i:04d}.wav")
    write(filename, 16000, segment_np)
    
    print(f"Segment {i:04d} guardat a {filename}")
print(f"✔ {len(speech_timestamps)} segments generats a {output_dir}")
