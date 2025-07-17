# Que hi ha en aquest repo
Aquest projecte et permet preparar les dades necessàries per entrenar un model de síntesi de veu personalitzat amb la teva pròpia veu. Això es coneix com fine-tuning d’un model de text-to-speech (TTS), que és una tecnologia que transforma text escrit en veu parlada.

En altres paraules, podràs gravar-te llegint alguns textos, processar aquestes gravacions seguint les instruccions d’aquest repositori, i entrenar un model perquè parli com tu. És útil per aplicacions com assistents virtuals, doblatge automàtic o projectes personals amb veu sintètica personalitzada.

# Instruccions

## Instalar miniconda
Descarrega i instal·la miniconda o anaconda si no ho tens instal·lat.
https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

## Clonar projecte
Descarrega els fitxers del projecte en una carpeta i obre la carpeta.
```
git clone https://github.com/palaueb/clonador_veu.git
cd clonador_veu
```

## Crear l'entorn aina, i instal·lar els requisits
Pot ser que no tinguis correctament les variables d'entorn i conda no s'executi, en aquest cas, ves a la carpeta on l'has instal·lat i inicia un entorn base. Des de l'entorn base, torna a la carpeta del projecte i inicia l'entorn.

Un cop has iniciat l'entorn base o has configurat el PATH amb la ruta de miniconda ja pots iniciar l'entorn. En aquest cas li he posat aina, però un altre nom que pot servir es simplement clonador.
```
conda create -n aina python=3.10 -y
conda activate aina
```
Si no vols fer res d'això, collons, monta un dockerfile i fes un pull request i actualitzaré tota la moguda.

## Instal·lem les dependències per crear els datasets
```
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
pip install transformers datasets phonemizer openai-whisper git+https://github.com/snakers4/silero-vad.git
```

## Compilar i instal·lar espeak-ng tunejat per projecte aina
```
git clone https://github.com/projecte-aina/espeak-ng
```

El readme del projecte porta com compilar en linux, per fer-ho en windows usar CYGWIN, instal·lar les dependències per compilar i seguir les mateixes indicacions que per linux.
*Nota important:* no usar multicore (flag -jX) durant el make, ja que no suporta procès en lots i la compilació falla.

Requisits per compilar amb cygwin en windows: 
autoconf, automake, gcc-core, gcc-g++, gettext-devel, libtool, make, patch i pkg-config.

# un cop tot funcioni, preparar un requirements.txt o environment.yaml (o un dockerfile, jo que se...)

