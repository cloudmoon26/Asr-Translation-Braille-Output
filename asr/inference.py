'''
import time
import librosa

from asr.audio_preprocess import preprocess_audio
from asr.model import WhisperASR
from asr.postprocess import normalize_text
'''
import time
import librosa
import soundfile as sf
import tempfile

from asr.audio_preprocess import preprocess_audio
from asr.postprocess import normalize_text


def run_asr(audio_path, asr_model):

    # 오디오 로드
    audio, sr = librosa.load(audio_path, sr=None)

    audio_duration = len(audio) / sr

    start = time.time()

    chunks = preprocess_audio(audio_path)

    # 이미 로드된 Whisper 사용
    raw_text = asr_model.transcribe(chunks)

    elapsed = time.time() - start

    final_text = normalize_text(raw_text)

    rtf = elapsed / audio_duration

    return final_text, rtf

""" last version
import time
import librosa
import soundfile as sf
import tempfile

from asr.audio_preprocess import preprocess_audio
from asr.model import WhisperASR
from asr.postprocess import normalize_text

def run_asr(audio_path):

    # 오디오 로드
    audio, sr = librosa.load(audio_path, sr=None)

    start_sec = 60
    end_sec = 120
    audio = audio[sr * start_sec : sr * end_sec]

    # 임시 파일 저장
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(temp_wav.name, audio, sr)

    audio_duration = len(audio) / sr

    asr = WhisperASR()

    start = time.time()

    chunks = preprocess_audio(temp_wav.name)
    raw_text = asr.transcribe(chunks)

    elapsed = time.time() - start

    final_text = normalize_text(raw_text)

    rtf = elapsed / audio_duration

    return final_text, rtf

"""    
'''
def run_asr(audio_path):
    audio, sr = librosa.load(audio_path, sr=None)
    audio_duration = len(audio) / sr

    asr = WhisperASR()

    start = time.time()
    chunks = preprocess_audio(audio_path)
    raw_text = asr.transcribe(chunks)
    elapsed = time.time() - start

    final_text = normalize_text(raw_text)

    rtf = elapsed / audio_duration

    return final_text, rtf
'''
