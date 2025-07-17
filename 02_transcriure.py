from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import torchaudio
import os
import argparse

parser = argparse.ArgumentParser(description="Transcriu segments d'àudio.")
parser.add_argument("--input-dir", default="segments", help="Carpeta d'entrada dels segments (opcional)")
parser.add_argument("--model-name", default="projecte-aina/whisper-large-v3-ca-3catparla", help="Nom del model Whisper a utilitzar")
parser.add_argument("--output-file", default="transcriptions_raw.txt", help="Fitxer de sortida per a les transcripcions")
args = parser.parse_args()

segments_dir = args.input_dir
model_name = args.model_name
output_file = args.output_file

torchaudio.set_audio_backend("soundfile")  # actiu a Windows amb pip install soundfile

print("Carregant el model Whisper...")
# Usa safetensors per evitar vulnerabilitat CVE-2025-32434
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(
    model_name,
    use_safetensors=True  # 👈 molt important
)

# Envia model a GPU si està disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()


transcriptions = []

print("Processant segments d'àudio...")
for filename in sorted(os.listdir(segments_dir)):
    if filename.endswith(".wav"):
        path = os.path.join(segments_dir, filename)
        print(f"Processant {filename}...")
        speech, sr = torchaudio.load(path)
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(sr, 16000)
            speech = resampler(speech)

        print(f"Transcrivint {filename}...")
        input_features = processor(speech.squeeze(), sampling_rate=16000, return_tensors="pt").input_features.to(device)
        predicted_ids = model.generate(input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        transcriptions.append((filename, transcription.strip()))

# Guardar transcripció
with open(output_file, "w", encoding="utf-8") as f:
    for fname, text in transcriptions:
        f.write(f"{fname}|{text}\n")

print("✔ Transcripció completada i guardada a transcriptions_raw.txt")
