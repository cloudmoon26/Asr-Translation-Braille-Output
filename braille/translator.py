from KorToBraille.KorToBraille import KorToBraille

class KoreanBrailleTranslator:
    def __init__(self):
        self.kor2braille = KorToBraille()

    def translate(self, text):
        return self.kor2braille.korTranslate(text)
