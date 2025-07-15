
1. instalar miniconda
2. crear una carpeta amb un entorn aina, i instal·lar els requisits

conda create -n aina python=3.10 -y
conda activate aina

conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
pip install transformers datasets phonemizer openai-whisper git+https://github.com/snakers4/silero-vad.git

Instal·lar espeak-ng
Windows msi i macos pkg a https://github.com/espeak-ng/espeak-ng/releases/
Linux sudo apt-get install espeak-ng 

# un cop tot funcioni, preparar un requirements.txt o environment.yaml

