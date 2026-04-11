def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    # Şifre çözme modundaysak kaydırma işlemini tersine çeviriyoruz
    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if char.isalpha():  # Sadece harfleri işleme al (boşluk ve noktalama işaretlerini atla)
            ascii_offset = 65 if char.isupper() else 97
            # Modüler aritmetik ile alfabede kaydırma işlemi
            shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            result += shifted_char
        else:
            result += char
    return result


def vigenere_cipher(text, key, mode='encrypt'):
    result = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            # Anahtar kelimedeki harfin alfabedeki indeksini bul
            shift = ord(key[key_index]) - 65

            if mode == 'decrypt':
                shift = -shift

            ascii_offset = 65 if char.isupper() else 97
            shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            result += shifted_char

            # Anahtar kelimenin harfleri arasında döngü yap
            key_index = (key_index + 1) % len(key)
        else:
            result += char
    return result


# evet test kodları
if __name__ == "__main__":
    orijinal_metin = "ANKARA"

    print("--- CAESAR TEST ---")
    caesar_sifreli = caesar_cipher(orijinal_metin, shift=3, mode='encrypt')
    print(f"Şifreli: {caesar_sifreli}")
    print(f"Çözülmüş: {caesar_cipher(caesar_sifreli, shift=3, mode='decrypt')}\n")

    print("--- VIGENERE TEST ---")
    vigenere_sifreli = vigenere_cipher(orijinal_metin, key="BMB", mode='encrypt')
    print(f"Şifreli: {vigenere_sifreli}")
    print(f"Çözülmüş: {vigenere_cipher(vigenere_sifreli, key='BMB', mode='decrypt')}")