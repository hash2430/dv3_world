from concurrent.futures import ProcessPoolExecutor
from functools import partial
import numpy as np
import os
import audio
from nnmnkwii.datasets import vctk
from nnmnkwii.io import hts
from hparams import hparams
from os.path import exists
import librosa
import re


def build_from_path(in_dir, out_dir, num_workers=1, tqdm=lambda x: x):
    executor = ProcessPoolExecutor(max_workers=num_workers)
    futures = []

    speakers = vctk.available_speakers

    td = vctk.TranscriptionDataSource(in_dir, speakers=speakers)
    transcriptions = td.collect_files()
    speaker_ids = td.labels
    speaker_ids_unique = np.unique(speaker_ids)
    speaker_to_speaker_id = {}
    for i, j in zip(speakers, speaker_ids_unique):
        speaker_to_speaker_id[i] = j
    wav_paths = vctk.WavFileDataSource(
        in_dir, speakers=speakers).collect_files()

    _ignore_speaker = hparams.not_for_train_speaker.split(", ")
    ignore_speaker = [speaker_to_speaker_id[i] for i in _ignore_speaker]
    for index, (speaker_id, text, wav_path) in enumerate(
            zip(speaker_ids, transcriptions, wav_paths)):
        if speaker_id in ignore_speaker:
            continue
        futures.append(executor.submit(
            partial(_process_utterance, out_dir, index + 1, speaker_id, wav_path, text)))
    return [future.result() for future in tqdm(futures)]


def start_at(labels):
    has_silence = labels[0][-1] == "pau"
    if not has_silence:
        return labels[0][0]
    for i in range(1, len(labels)):
        if labels[i][-1] != "pau":
            return labels[i][0]
    assert False


def end_at(labels):
    has_silence = labels[-1][-1] == "pau"
    if not has_silence:
        return labels[-1][1]
    for i in range(len(labels) - 2, 0, -1):
        if labels[i][-1] != "pau":
            return labels[i][1]
    assert False


def _process_utterance(out_dir, index, speaker_id, wav_path, text):
    sr = hparams.sample_rate
    filename = os.path.basename(wav_path).replace('.wav', '')

    # Load the audio to a numpy array:
    wav = audio.load_wav(wav_path)

    lab_path = wav_path.replace("wav48/", "lab/").replace(".wav", ".lab")

    # Trim silence from hts labels if available
    if exists(lab_path):
        labels = hts.load(lab_path)
        b = int(start_at(labels) * 1e-7 * sr)
        e = int(end_at(labels) * 1e-7 * sr)
        wav = wav[b:e]
        wav, _ = librosa.effects.trim(wav, top_db=25)
    # Librosa trim seems to cut off the ending part of speech
    else:
        wav, _ = librosa.effects.trim(wav, top_db=15)

    if hparams.rescaling:
        wav = wav / np.abs(wav).max() * hparams.rescaling_max

    # Save trimmed wav
    save_wav_path = re.sub('wav48', 'wav_trim_22050', wav_path)
    dir = os.path.dirname(save_wav_path)
    if not os.path.exists(dir):
        os.system('mkdir {} -p'.format(dir))
    audio.save_wav(wav, save_wav_path)

    # Compute the linear-scale spectrogram from the wav:
    spectrogram = audio.spectrogram(wav).astype(np.float32)
    n_frames = spectrogram.shape[1]

    # Compute a mel-scale spectrogram from the wav:
    mel_spectrogram = audio.melspectrogram(wav).astype(np.float32)

    # Write the spectrograms to disk:
    spectrogram_filename = '{}-spec.npy'.format(filename)
    mel_filename = '{}-mel.npy'.format(filename)
    np.save(os.path.join(out_dir, spectrogram_filename), spectrogram.T, allow_pickle=False)
    np.save(os.path.join(out_dir, mel_filename), mel_spectrogram.T, allow_pickle=False)

    # Return a tuple describing this training example:
    return (spectrogram_filename, mel_filename, n_frames, text, speaker_id)
