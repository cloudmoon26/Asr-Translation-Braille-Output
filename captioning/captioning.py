import cv2
import clip
import torch
import torch.nn.functional as F
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration

class CaptionModel:
    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        print("Initializing Captioning & Scene Detection Models...")

        # 1. CLIP 모델 로드 (장면 전환 감지용)
        self.clip_model, self.clip_preprocess = clip.load("ViT-B/32", device=self.device)

        # 2. BLIP-2 모델 로드 (이미지 캡셔닝용)
        self.blip_processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        self.blip_model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b",
            torch_dtype=torch.float16 if "cuda" in self.device else torch.float32
        ).to(self.device)

        print("Captioning models loaded successfully.")

    def _encode_frame(self, frame):
        """CLIP을 사용하여 프레임의 특징 벡터(Feature)를 추출합니다."""
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = self.clip_preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            feature = self.clip_model.encode_image(image)

        # 정규화
        feature = feature / feature.norm(dim=-1, keepdim=True)
        return feature

    def _detect_scenes_and_get_keyframes(self, frames, threshold=0.75):
        """프레임 간 유사도를 비교하여 장면 전환을 감지하고, 각 장면의 핵심 프레임을 추출합니다."""
        scene_changes = []
        prev_feature = None

        print("Detecting scene changes...")
        for i, frame in enumerate(frames):
            feature = self._encode_frame(frame)

            if prev_feature is not None:
                sim = F.cosine_similarity(feature, prev_feature)
                # 유사도가 기준치(0.75) 미만이면 새로운 장면으로 인식
                if sim.item() < threshold:
                    scene_changes.append(i)

            prev_feature = feature

        # 장면 경계 나누기
        scene_boundaries = [0] + scene_changes + [len(frames)]
        scenes = []
        for i in range(len(scene_boundaries) - 1):
            start = scene_boundaries[i]
            end = scene_boundaries[i + 1]
            scenes.append((start, end))

        # 각 장면의 중간(Mid) 프레임을 Key Frame으로 선정
        key_frames = []
        for start, end in scenes:
            mid = (start + end) // 2
            key_frames.append(frames[mid])

        print(f"Detected {len(scenes)} distinct scenes.")
        return key_frames

    def _generate_caption_from_frame(self, frame):
        """BLIP-2를 사용하여 단일 프레임에 대한 텍스트 캡션을 생성합니다."""
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        inputs = self.blip_processor(images=image, return_tensors="pt").to(self.device)
        if "cuda" in self.device:
            inputs = {k: v.to(dtype=torch.float16) if v.dtype == torch.float32 else v for k, v in inputs.items()}

        with torch.no_grad():
            generated_ids = self.blip_model.generate(**inputs, max_new_tokens=30)

        caption = self.blip_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return caption.strip()

    def generate_captions(self, frames):
        """메인 파이프라인에서 호출할 메인 함수: 프레임 리스트를 받아 최종 캡션 리스트를 반환합니다."""
        if not frames:
            return []

        # 1. 장면 전환 감지 및 핵심 프레임 추출
        key_frames = self._detect_scenes_and_get_keyframes(frames)

        # 2. 각 핵심 프레임별 캡션 생성
        captions = []
        for i, frame in enumerate(key_frames):
            caption = self._generate_caption_from_frame(frame)
            captions.append(caption)
            print(f"  [Scene {i+1}] Generated Caption: {caption}")

        return captions
