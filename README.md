# Que hi ha en aquest repo
Aquest projecte et permet preparar les dades necessàries per entrenar un model de síntesi de veu personalitzat amb la teva pròpia veu. Això es coneix com fine-tuning d’un model de text-to-speech (TTS), que és una tecnologia que transforma text escrit en veu parlada.

En altres paraules, podràs gravar-te llegint alguns textos, processar aquestes gravacions seguint les instruccions d’aquest repositori, i entrenar un model perquè parli com tu. És útil per aplicacions com assistents virtuals, doblatge automàtic o projectes personals amb veu sintètica personalitzada.

# Instruccions per preparar l'entorn

Sí, li falta un dockerfile. OK boomer.

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

*Nota important:* no usar multicore (make -jX) durant el make, ja que no suporta procès en lots i la compilació falla.

Requisits per compilar amb cygwin en windows: 
autoconf, automake, gcc-core, gcc-g++, gettext-devel, libtool, make, patch i pkg-config.

# Instruccions per preparar el dataset
Els documents estan numerats en l'ordre d'execució, potser ho unifico, ara mateix esta així.

*Interesant de saber:* l'unic argument necessari es --input-wav, la resta es poden deixar per defecte i son els valors de la documentació.

## Segmentar els audios
En aquest punt, el sistema necessita que li facilitis un wav amb totes les lectures. El que fa aquest codi es segmentar el wav en parts mes petites, per executar-ho:

```
python 01_segmentar.py --input-wav lectures.wav --output-dir segments
```

## Transcriure els audios
Ara extreurem els textos dels audios, de manera que ens comenci a generar el fitxer que acabarem usant en l'entrenament:

```
python 02_transcriure.py --input-dir segments --output-file transcriptions_raw.txt --model-name projecte-aina/whisper-large-v3-ca-3catparla
```
En l'exemple utilitzo el model whisper-large-v3-ca-3catparla que segons el projecte Aina és:

*The "whisper-large-v3-ca-3catparla" is an acoustic model suitable for Automatic Speech Recognition in Catalan. It is the result of finetuning the model "openai/whisper-large-v3" with 710 hours of Catalan data released by the Projecte AINA from Barcelona, Spain.
This model can be used for Automatic Speech Recognition (ASR) in Catalan. The model is intended to transcribe audio files in Catalan to plain text without punctuation.*

O sigui: El "whisper-large-v3-ca-3catparla" és un model acústic adequat per al reconeixement automàtic de la parla en català. És el resultat d’un afinament del model "openai/whisper-large-v3" amb 710 hores de dades en català proporcionades pel Projecte AINA de Barcelona, Espanya.
Aquest model es pot utilitzar per al reconeixement automàtic de la parla (ASR) en català. Està pensat per transcriure arxius d’àudio en català a text pla sense puntuació.

## Fonemitzar els textos
Per que l'entrenament sigui satisfactori, es requereix que els textos proporcionats siguin en alfabet fonètic internacional (IPA), es aquí on hem de fer servir l'espeak-ng, per que funcioni correctament ha d'estar configurat al PATH.

```
python 03_phonemitzar.py --input-file transcripcions_raw.txt --output-file train.txt
```

Ens genera una sortida del tipus:

```
0005.wav|əl kəpˈitul ˈu əl tˈemz məteuɾulˈɔʒik
0006.wav|əstˈa əstɾuktuɾˈat əm bˈujt əpərtˈat‍s
```

## Normalitzar el dataset

Aquest darrer pas es el necessari per preparar les dades per que puguin ser ingestades per matxa-tts, ja que demana que les dades tinguin un format determinat.

```
python 04_normalitzar.py --output-folder custom_tts_dataset --wav-segments segments --train-file train.txt --speaker-id 9
```

Uhm, per algún motiu de seguretat no vaig voler sobreescriure --output-folder si existeix previament, així que si ja teniu una carpeta amb aquest nom us dirà que poseu un nom nou i aturarà l'execució.

## Realitzar l'afinament del model (fine tunning)

Això encara no esta fet, em cal acabar d'entendre quins paràmetres requereix matxa i de quina forma ajustar-ho al que ja tinc fet.

Tot comentari sera benvingut.

# notes
*un cop tot funcioni, preparar un requirements.txt o environment.yaml (o un dockerfile, jo que se...)*

