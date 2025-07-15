import argparse
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from datasets import load_dataset, Audio

print("Iniciant l'entrenament del model TTS...")

parser = argparse.ArgumentParser(description="Entrenament del model TTS")
parser.add_argument("--model_name", type=str, default="projecte-aina/matxa-tts-cat-multiaccent", help="Nom del model preentrenat a utilitzar.")
parser.add_argument("--dataset_path", type=str, default="custom_tts_datasetv", help="Camí a la carpeta del dataset personalitzat.")

args = parser.parse_args()

model_name = args.model_name
dataset_path = args.dataset_path


print(f"Carregant el model {model_name} i el dataset des de {dataset_path}...")
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_name)

print(f"Nom del model: {model_name}")
print(f"Tipus de processador: {type(processor)}")
print(f"Tipus de model: {type(model)}")

data_files = {
    "train": f"{dataset_path}/metadata.csv",
    "audio": f"{dataset_path}/audio"
}
dataset = load_dataset(
    "csv",
    data_files=data_files.train,
    split="train"
)

dataset = dataset.cast_column("file", Audio(folder=data_files.audio, sampling_rate=16000))

# mostra informació sobre el dataset
print(f"Nombre d'exemples al dataset: {len(dataset)}")
