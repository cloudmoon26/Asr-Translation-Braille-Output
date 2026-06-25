# ==================================================================================
import torch
import cv2

from asr.model import WhisperASR
from asr.inference import run_asr

from captioning.captioning import CaptionModel
#from captioning import extract_frames

from video.audio import extract_audio

from braille.converter import text_to_braille
from braille.arduino import send_to_arduino

from transformers import (
    MBartForConditionalGeneration,
    MBart50TokenizerFast
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =========================================================
# 번역 함수
# =========================================================

def translate_text(text, model, tokenizer):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(DEVICE)

    generated_tokens = model.generate(
        **inputs,
        max_length=128,
        num_beams=4,
        early_stopping=True,
        forced_bos_token_id=tokenizer.lang_code_to_id["ko_KR"]
    )

    translated = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True
    )[0]

    return translated


# =========================================================
# 모델 초기화 (프로그램 시작 시 1회만)
# =========================================================

def initialize_models():

    print("Loading models...")

    # Whisper ASR
    asr_model = WhisperASR()

    # Image Captioning
    caption_model = CaptionModel()

    # Translation model
    MODEL_NAME = "arimurimu/mbart-distilled-en-ko-v3"

    tokenizer = MBart50TokenizerFast.from_pretrained(
        MODEL_NAME
    )

    translator = MBartForConditionalGeneration.from_pretrained(
        MODEL_NAME
    ).to(DEVICE)

    tokenizer.src_lang = "en_XX"
    tokenizer.tgt_lang = "ko_KR"

    print("All models loaded")

    return (
        asr_model,
        caption_model,
        translator,
        tokenizer
    )


# =========================================================
# 영상 처리
# =========================================================

def process_video(
    video_path,
    asr_model,
    caption_model,
    translator,
    tokenizer
):

    print("\n[1] Extracting audio...")

    audio_path = extract_audio(video_path)

    # =====================================================
    # ASR
    # =====================================================

    print("[2] Running ASR...")

    asr_text, rtf = run_asr(
        audio_path,
        asr_model
    )

    print("ASR RESULT:")
    print(asr_text)


    # =====================================================
    # 이미지 캡셔닝
    # =====================================================

    print("\n[3] Running image captioning...")

    # -----------------------------------------------------
    # 비디오 열기
    # -----------------------------------------------------

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    # 5초 간격 프레임 추출
    frame_interval = int(fps * 5)
    frames = []
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # interval마다 프레임 저장
        if count % frame_interval == 0:
            frames.append(frame)

        count += 1
      
    cap.release()
    print(f"Extracted {len(frames)} frames")

    # -----------------------------------------------------
    # 캡션 생성
    # -----------------------------------------------------

    captions = caption_model.generate_captions(frames)

    # 여러 장면 설명을 하나의 문맥으로 결합
    visual_context = ". ".join(captions)

    print("\n===== CAPTION RESULT =====")
    print(visual_context)

    # =====================================================
    # 번역
    # =====================================================

    print("\n[4] Translating dialogue...")

    translated_dialogue = translate_text(
        asr_text,
        translator,
        tokenizer
    )

    translated_dialogue_2 = translate_text(
        visual_context,
        translator,
        tokenizer
    )

    # =====================================================
    # 최종 출력 구성
    # =====================================================

    final_output = f"{translated_dialogue_2}\n{translated_dialogue}"

    print("\n===== FINAL RESULT =====")
    print(final_output)

    # =====================================================
    # 점자 변환
    # =====================================================

    print("[5] Converting to braille...")

    braille_text = text_to_braille(
        final_output
    )

    print("\n===== BRAILLE =====")
    print(braille_text)

    # =====================================================
    # 아두이노 전송
    # =====================================================

    print("[6] Sending to Arduino...")

    send_to_arduino(
        braille_text
    )

    print("Arduino output completed")

    return {
        "asr": asr_text,
        "context": visual_context,
        "translation": translated_dialogue,
        "braille": braille_text
    }


# =========================================================
# Main loop
# =========================================================

def main():

    (
        asr_model,
        caption_model,
        translator,
        tokenizer
    ) = initialize_models()

    while True:

        print("\n============================")
        print("Video Translation System")
        print("============================")

        video_path = input(
            "\nInput video path (exit to quit): "
        )

        if video_path.lower() == "exit":
            break

        try:

            result = process_video(
                video_path,
                asr_model,
                caption_model,
                translator,
                tokenizer
            )

        except Exception as e:

            print("\nERROR:")
            print(e)

        finally:
            torch.cuda.empty_cache()

    print("\nSystem terminated")


# =========================================================
# Run
# =========================================================

if __name__ == "__main__":
    main()
