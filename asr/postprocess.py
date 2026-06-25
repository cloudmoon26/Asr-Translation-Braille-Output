import re

FILLERS = ["uh", "um", "erm"]

def normalize_text(text):
    text = text.lower()

    # 숫자 단순 정규화 (확장 가능)
    text = re.sub(r"\bzero\b", "0", text)

    # 특수기호 통일
    text = re.sub(r"[“”]", "\"", text)
    text = re.sub(r"[’]", "'", text)

    # filler 제거 (옵션)
    for f in FILLERS:
        text = re.sub(rf"\b{f}\b", "", text)

    # 중복 공백 제거
    text = re.sub(r"\s+", " ", text)

    return text.strip()
