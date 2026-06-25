from braille.translator import KoreanBrailleTranslator
from braille.encoder import encode_braille

class BraillePipeline:
    def __init__(self):
        self.translator = KoreanBrailleTranslator()

    def convert(self, text):
        braille = self.translator.translate(text)
        masks = encode_braille(braille)
        return braille, masks
