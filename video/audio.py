import subprocess
import os

def extract_audio(video_path):

    output_audio = "temp_audio.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,

        # 비디오 제거
        "-vn",

        # Whisper 최적 형식
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",

        output_audio
    ]

    subprocess.run(command, check=True)

    return output_audio
