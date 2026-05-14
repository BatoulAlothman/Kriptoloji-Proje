def turkce_karakter_temizle(metin):
    """
    Şifreleme sırasında modüler aritmetiğin çökmemesi için
    Türkçe karakterleri İngilizce karşılıklarına çevirir.
    """
    degisimler = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return metin.translate(degisimler)


def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    # Türkçe karakter riskini ortadan kaldırıyoruz
    text = turkce_karakter_temizle(text)

    # Şifre çözme modundaysak kaydırma işlemini tersine çeviriyoruz
    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if char.isalpha():  # Sadece harfleri işleme al
            ascii_offset = 65 if char.isupper() else 97
            # Modüler aritmetik ile alfabede kaydırma işlemi
            shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            result += shifted_char
        else:
            result += char
    return result


def vigenere_cipher(text, key, mode='encrypt'):
    result = ""
    text = turkce_karakter_temizle(text)

    # Anahtar kelimedeki Türkçe karakterleri temizle ve boşluk/rakam varsa atla
    key = turkce_karakter_temizle(key).upper()
    key = "".join([c for c in key if c.isalpha()])

    # Eğer anahtar sadece rakamlardan oluşuyorsa çökmemesi için güvenlik önlemi
    if not key:
        return text

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


# --- TEST KODLARI ---
if __name__ == "__main__":
    # Türkçe karakterler içeren test metni
    orijinal_metin = "ŞİFRELEME ÖDEVİ"

    print("--- CAESAR TEST ---")
    caesar_sifreli = caesar_cipher(orijinal_metin, shift=3, mode='encrypt')
    print(f"Orijinal: {orijinal_metin}")
    print(f"Şifreli: {caesar_sifreli}")
    print(f"Çözülmüş: {caesar_cipher(caesar_sifreli, shift=3, mode='decrypt')}\n")

    print("--- VIGENERE TEST ---")
    # Boşluk ve rakam içeren hatalı bir anahtar veriyoruz, sistem bunu sadece "BMB" olarak algılayacak
    vigenere_sifreli = vigenere_cipher(orijinal_metin, key="BMB 123", mode='encrypt')
    print(f"Orijinal: {orijinal_metin}")
    print(f"Şifreli: {vigenere_sifreli}")
    print(f"Çözülmüş: {vigenere_cipher(vigenere_sifreli, key='BMB 123', mode='decrypt')}")