# 한글 점자 변환 라이브러리 설치 필요
# pip install hbcvt

from hbcvt import h2b

def text_to_braille(text):

    """
    한국어 텍스트를 한글 점자로 변환
    """

    # 한글 → 점자 변환
    braille = h2b.text(text)

    # 리스트 형태 → 문자열 변환
    braille_text = ""

    for sentence in braille:
        for word in sentence:
            for char in word:
                braille_text += "".join(str(dot) for dot in char)
                braille_text += " "

    return braille_text.strip()
