import librosa
import numpy as np
import soundfile as sf

TARGET_SR = 16000
MAX_CHUNK_SEC = 30
OVERLAP_SEC = 3

def load_audio(path):
    audio, sr = librosa.load(path, sr=None, mono=False)

    # stereo → mono
    if audio.ndim > 1:
        audio = np.mean(audio, axis=0)

    # resample
    if sr != TARGET_SR:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)

    return audio, TARGET_SR


def trim_silence(audio, sr):
    trimmed, _ = librosa.effects.trim(
        audio,
        top_db=20
    )
    return trimmed


def normalize_volume(audio):
    rms = np.sqrt(np.mean(audio**2))
    if rms > 0:
        audio = audio / rms
    return audio


def split_audio(audio, sr):
    chunk_len = MAX_CHUNK_SEC * sr
    overlap_len = OVERLAP_SEC * sr

    chunks = []
    start = 0

    while start < len(audio):
        end = start + chunk_len
        chunk = audio[start:end]
        chunks.append(chunk)
        start = end - overlap_len

    return chunks


def preprocess_audio(path):
    audio, sr = load_audio(path)
    audio = trim_silence(audio, sr)
    audio = normalize_volume(audio)
    chunks = split_audio(audio, sr)
    return chunks
