# Que hi ha en aquest repo
Aquest projecte et permet preparar les dades necessàries per entrenar un model de síntesi de veu personalitzat amb la teva pròpia veu. Això es coneix com fine-tuning d’un model de text-to-speech (TTS), que és una tecnologia que transforma text escrit en veu parlada.

En altres paraules, podràs gravar-te llegint alguns textos, processar aquestes gravacions seguint les instruccions d’aquest repositori, i entrenar un model perquè parli com tu. És útil per aplicacions com assistents virtuals, doblatge automàtic o projectes personals amb veu sintètica personalitzada.

Tota l'ajuda esta pensada per fer-ho en windows, ja que en el meu cas tinc la tarja gràfica en un sistema Windows 11. M'hauria agradat documentar-ho per Linux, ja que em sembla infinitament mes robuts i fàcil de fer tot plegat, però bé, no es pot tenir tot, el focus estaba en fer-ho funcionar.

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
Si tens els audios en diferents fitxers mp3 o wav i et cal, la comanda del ffmpeg per unir-los és:

```
Get-ChildItem -Filter *.mp3 | Sort-Object Name | ForEach-Object { "file '$($_.FullName)'" } | Set-Content llista.txt
# un cop tenim la llista.txt feta amb tots els mp3 executem:
ffmpeg -f concat -safe 0 -i llista.txt -acodec pcm_s16le -ar 16000 -ac 1 sortida.wav
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

El procès que segueix aquesta part esta basada en la documentació proporcionada per la branca dev-cat de Matcha-TTS a l'enllaç https://github.com/langtech-bsc/Matcha-TTS/tree/dev-cat#train-with-your-own-dataset

La part de compilar l'espeak es suposa que l'heu d'haver superat, si no us ensortiu, us puc facilitar el binari que he compilat, però no puc garantir cap tipus de compatibilitat amb el vostre sistema operatiu.

A continuació us poso el que heu de fer pas a pas:
```


%USERPROFILE%\miniconda3\Scripts\activate base
conda create -n matxa python=3.10 -y
conda activate matxa
pip install -e .
```

Dependencies de merda: pip install piper-phonemize -f https://k2-fsa.github.io/icefall/piper_phonemize

compilar la DLL d'espeak-ng: 

```
espeak-ng\src>git clone https://github.com/espeak-ng/pcaudiolib.git
```
Editar fitxer espeak-ng\src\pcaudiolib\src\xaudio2.cpp
```
class VoiceCallbacks : public IXAudio2VoiceCallback
{
public:
	void OnBufferEnd(void* pBufferContext) {
		if (pBufferContext != NULL)
		{
			free((void*)pBufferContext);
		}
	}

	// Stubs for all interface callbacks
	void OnStreamEnd() { }
	void OnVoiceProcessingPassEnd() { }
	void OnVoiceProcessingPassStart(UINT32 SamplesRequired) { }
	void OnBufferStart(void* pBufferContext) { }
	void OnLoopEnd(void* pBufferContext) { }
	void OnVoiceError(void* pBufferContext, HRESULT Error) { }
} voiceCallbacks;

# Canviar per:

class VoiceCallbacks : public IXAudio2VoiceCallback
{
public:
	void STDMETHODCALLTYPE OnBufferEnd(void* pBufferContext) override {
		if (pBufferContext != NULL)
		{
			free((void*)pBufferContext);
		}
	}

	void STDMETHODCALLTYPE OnStreamEnd() override { }
	void STDMETHODCALLTYPE OnVoiceProcessingPassEnd() override { }
	void STDMETHODCALLTYPE OnVoiceProcessingPassStart(UINT32 SamplesRequired) override { }
	void STDMETHODCALLTYPE OnBufferStart(void* pBufferContext) override { }
	void STDMETHODCALLTYPE OnLoopEnd(void* pBufferContext) override { }
	void STDMETHODCALLTYPE OnVoiceError(void* pBufferContext, HRESULT Error) override { }
} voiceCallbacks;

```
Seguim amb la compilació
```
espeak-ng\src\windows>msbuild libespeak-ng.vcxproj /p:Configuration=Release /p:Platform=x64
```

Ara ja tenim la DLL a la ruta espeak-ng\src\windows\x64\Release\libespeak-ng.dll

Un cop fet tot això, jo ja m'he arrepentit 20 cops de fer-ho en windows i no fer-ho amb el subsistema linux de windows, segueixo ja per que això ho faig per orgull.

Modifiquem el codi de matcha_vocos_inference.py del codi del repositori del Matxa-TTS:
```
import os

os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = "D:\\text-to-voice\\clonador-veu\\libespeak-ng.dll"
os.environ['ESPEAK_DATA_PATH'] = "D:\\text-to-voice\\espeak-ng\\espeak-ng-data"
```

Us deixo l'exemple de les rutes que he fet servir jo, no cal que siguin les mateixes, no siguis meló!

# notes
*un cop tot funcioni, preparar un requirements.txt o environment.yaml (o un dockerfile, jo que se...)*

