# Deep voice 3 with World vocoder
This repository supports World vocoder for DV3.
There are modifications to Merlin code for extracting world features and synthesizing from them.
## Merlin code modification
I will explain assuming your Merlin directory and this project directory as follows
```
Merlin: /home/admin/merlin
Merlin speech synthesis: /home/admin/merlin/egs/build_your_own_voice/s2
Current project directory: dv3_world
```
### Modify WORLD tool
I have added patch for modifying 'WORLD' tool inside merlin.
This modification is necessary because WORLD hopping size is hardcoded as 5 ms while DV3 takes it in timesteps(samples).
Assuming 1024 fft size and 256 hopping size, 'frame_period' variable of WORLD needs to be changed as 11.6099773243 .

* How to apply patch
```
cp dv3_world/merlin/merlin_vctk_e2e.diff /home/admin/merlin
cd /home/adim/merlin
git apply merlin_vctk_e2e.diff
```
 ### Additional shell scripts to add to your merlin directory
 There are 2 shell scripts for merlin in this project.
 1. 03_vctk_prepare_acoustic_features.sh
  This is required for extracting features from VCTK. Use this instead of your original 03_prepare_acoustic_features.sh. This is required because VCTK has another directory layer for speaker.
2. gen_file_id_list.sh
  This is required because I am skipping '02_prepare_labels.sh' and doing it e2e while that step is where training file list is generated.
 * How to add shell scripts to your merlin project
 ```
 cp dv3_world/merlin/egs/build_your_own_voice/vctk/* /home/admin/merin/egs/build_your_own_voice/s2
 ```
 
 Once you have followed above process to modify Merlin, 
 Follow **guidelines/extract_world.pdf** for feature extraction using merlin, **guidelines/synth_world.pdf** for synthesizing wav from the features DV3 has predicted.
 
