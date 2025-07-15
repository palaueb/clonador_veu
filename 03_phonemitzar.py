import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description="Genera fonemes a partir de transcripcions.")
parser.add_argument("--input-file", default="transcriptions_raw.txt", help="Fitxer d'entrada amb transcripcions")
parser.add_argument("--output-file", default="train.txt", help="Fitxer de sortida per a fonemes")
args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
if not os.path.isfile(input_file):
    print(f"Error: El fitxer d'entrada {input_file} no existeix.")
    exit(1)

#revisa que la carpeta on exportarem amb --output-file existeix, i si no creala:
output_dir = os.path.dirname(output_file)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

def text_to_phonemes(text):
    # -q: Silencia la sortida de l'espeak-ng
    # -v ca: Utilitza el català com a llengua
    # --ipa=3: Utilitza el format IPA
    cmd = ["espeak-ng", "-q", "-v", "ca", "--ipa=3", text]
    try:
        output = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if output.returncode != 0:
            print(f"Error executant espeak-ng per '{text}': {output.stderr}")
            return ""
        return output.stdout.strip()
    except Exception as e:
        print(f"Exception executant espeak-ng per '{text}': {e}")
        return ""


train_lines = []
print(f"Llegint transcripcions des de {input_file}...\n\n")
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if "|" not in line:
            print(f"Línia incorrecta: {line}")
            continue
        filename, text = line.split("|", 1)
              
        print(f"\rGenerant fonemes per a {filename}...", end='', flush=True)
        phonemes = text_to_phonemes(text)
        train_lines.append(f"{filename}|{phonemes}")

with open(output_file, "w", encoding="utf-8") as out:
    out.write("\n".join(train_lines))

print(f"✔ {output_file} generat amb fonemes!")