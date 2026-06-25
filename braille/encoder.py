def braille_to_mask(ch):
    cp = ord(ch)
    if 0x2800 <= cp <= 0x28FF:
        return (cp - 0x2800) & 0b00111111
    return 0

def encode_braille(braille_str):
    return [braille_to_mask(c) for c in braille_str]
