# Deep voice 3 with World vocoder
This repository extends DV3 implementation of r9y9 by supporting WORLD vocoder at its converter module. 
It provides WORLD feature extraction and wav synthesis using Merlin toolkit. Other DB might be supported later but for now it assumes from VCTK DB. It also assumes E2E manner TTS which means the case using G2P is not considered. Thus the whole process including wav trimming does not require HTSLabel. 
## 1. Download VCTK dataset
https://homepages.inf.ed.ac.uk/jyamagis/page3/page58/page58.html
## 2. Install Merlin
Since it extracts WORLD vocoder feature and synthesize wav from it using Merlin, you need to clone Merlin. Clone it from here https://github.com/CSTR-Edinburgh/merlin and wait before you compile the tools of Merlin since you need to modify the WORLD tool before compilation

## 3. Merlin code modification
You need to mdofiy some part of merlin. WORLD has hopping size of 5ms hardcoded while you need 256 timesteps of hopping size and so on.
So I have made 'merlin' directroy under this project. You must copy the files from it and replace it with the files in your merlin directory. Then you compile the tool as written in the Merlin guideline and start installing merlin as in https://github.com/CSTR-Edinburgh/merlin#installation.
**In case you already have installed merlin, you still have to replace the files with the ones I provide and compile**
```
bash tools/compile_tools.sh
```
## 4. DV3 preprocess
As in the original DV3 code, you need to run **preprocess.py**. In addition to mel and linear spectrogram extraction, wav is trimmed and that trimmed wav is stored. This procedure is required because WORLD features are extracted from stored wav directly and thus trimmed wav needs to be stored.
```
python preprocess.py vctk {VCTK-Corpus directory} {mel,linear spectrogram saving directory} --preset=presets/deepvoice3_vctk.json
```
For example,
```
python preprocess.py vctk /home/administrator/Music/VCTK-Corpus ./preprocess_output_trim --preset=presets/deepvoice3_vctk.json
```
As a result, mel and linear spectrograms are saved at **./preprocess_output_trim**
and trimmed wav are saved at **{VCTK-Corpus directory}/wav_trim_22050.** This directory is where Merlin refers to when extracting WORLD features from wav.

## 5. Extract WORLD features with Merlin
When I say 'merlin' it means the merlin that you cloned from its original repository.
Do not confuse with 'dv3_world/merlin'. At this point, you do not need 'dv3_world/merlin' once you have copied all the files from it to your 'merlin'.
### 5.1. Run setup
Create global configuration and modify sampling rate
```
cd merlin/egs/build_your_own_voice/s1
bash 01_setup.sh s1
vim conf/global_settings.cfg
```
Then change sampling rate as follows in order to the recommened setting of deepvoice3 that is configured in deepvoice3_vctk.json
```
SamplingFreq=22050
```
