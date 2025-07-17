
1. instalar miniconda
2. crear una carpeta amb un entorn aina, i instal·lar els requisits

conda create -n aina python=3.10 -y
conda activate aina

conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
pip install transformers datasets phonemizer openai-whisper git+https://github.com/snakers4/silero-vad.git

Compilar i instal·lar espeak-ng tunejat per projecte aina: 
el readme porta com compilar en linux, per fer-ho en windows usar CYGWIN, instal·lar les dependències per compilar i seguir les mateixes indicacions que per linux.
Una nota important, no usar multicore (flag -jX) durant el make, ja que no suporta procès en lots i la compilació falla.

Requisits per compilar amb cygwin en windows: https://github.com/projecte-aina/espeak-ng
autoconf, automake, gcc-core, gcc-g++, gettext-devel, libtool, make, patch i pkg-config.

# un cop tot funcioni, preparar un requirements.txt o environment.yaml (o un dockerfile, jo que se...)

