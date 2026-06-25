import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class WhisperASR:
    def __init__(self, model_name="openai/whisper-medium"):
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name)
        self.model.to(DEVICE)

    def transcribe(self, audio_chunks, language="en"):
        texts = []

        for chunk in audio_chunks:
            inputs = self.processor(
                chunk,
                sampling_rate=16000,
                return_tensors="pt"
            )

            input_features = inputs.input_features.to(DEVICE)

            predicted_ids = self.model.generate(
                input_features,
                language=language,
                task="transcribe"
            )

            text = self.processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]

            texts.append(text)

        return " ".join(texts)
        '''
    def transcribe(self, audio_chunks, language="ko"):
        texts = []

        forced_decoder_ids = self.processor.get_decoder_prompt_ids(
            language=language,
            task="transcribe"
        )

        for chunk in audio_chunks:
            inputs = self.processor(
                chunk,
                sampling_rate=16000,
                return_tensors="pt"
            )

            input_features = inputs.input_features.to(DEVICE)

            predicted_ids = self.model.generate(
                input_features,
                forced_decoder_ids=forced_decoder_ids
            )

            text = self.processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]

            texts.append(text)

        return " ".join(texts)
        '''
