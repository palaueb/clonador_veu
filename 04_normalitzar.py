import os
import shutil
import argparse
'''
my_tts_dataset/
├── audio/
│   ├── 0000.wav
│   ├── 0001.wav
├── metadata.csv
'''
parser = argparse.ArgumentParser(description='Preparació de dades per crear el dataset.')
parser.add_argument('--custom_folder', type=str, default='custom_tts_dataset', help='Nom de la carpeta que generarem.')
parser.add_argument('--wav_segments', type=str, default='segments', help='Carpeta on es troben els fitxers d\'àudio a processar.')
parser.add_argument('--train_file', type=str, default='train.txt', help='Fitxer amb les transcripcions de l\'àudio.')
parser.add_argument('--speaker_id', type=str, default='99', help='ID del parlant.')
args = parser.parse_args()

custom_folder = args.custom_folder
wav_segments = args.wav_segments
train_file = args.train_file
speaker_id = args.speaker_id

if not os.path.exists(custom_folder):
    audio_folder = os.path.join(custom_folder, 'audio')
    os.makedirs(audio_folder, exist_ok=True)

    metadata_file = os.path.join(custom_folder, 'metadata.csv')

    cf=open(metadata_file, 'w', encoding='utf-8')
    cf.write('file,text,speaker_id\n')

    #obre train_file i per cada linia converteix a csv, el format actual es xxx|yyy
    with open(train_file, 'r', encoding='utf-8') as tf:
        for line in tf:
            parts = line.strip().split('|', maxsplit=1)
            if len(parts) == 2:
                audio_file = parts[0].strip()
                text = parts[1].strip()
                print(f"\rProcessing audio file: {audio_file}", end='', flush=True)
                cf.write(f"{audio_file},\"{text}\",{speaker_id}\n")

                shutil.copy(os.path.join(wav_segments, audio_file), audio_folder)
            
        print("\rPreparació de dades completada.", end='', flush=True)
        print(f"\nFitxer de metadades creat a {metadata_file}.")
        print(f"Fitxers d'àudio copiats a {os.path.join(custom_folder, 'audio')}.")
else:
    print("The custom_tts_dataset folder already exists.")