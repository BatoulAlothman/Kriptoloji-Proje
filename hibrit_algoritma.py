import string
import random

def turkce_karakter_temizle(metin):
    """
    Şifreleme sırasında alfabede bulunmayan karakterler yüzünden
    programın çökmemesi için Türkçe harfleri dönüştürür.
    """
    degisimler = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return metin.translate(degisimler)

def ozel_alfabe_olustur(anahtar_kelime):
    standart_alfabe = string.ascii_uppercase
    # Anahtar kelimedeki Türkçe karakterleri temizle
    anahtar_kelime = turkce_karakter_temizle(anahtar_kelime).upper()

    ozel_alfabe = ""

    # 1. Anahtar kelimedeki harfleri (tekrarsız olarak) ekle
    for harf in anahtar_kelime:
        if harf.isalpha() and harf not in ozel_alfabe:
            ozel_alfabe += harf

    # 2. Alfabenin geri kalan harflerini ekle
    for harf in standart_alfabe:
        if harf not in ozel_alfabe:
            ozel_alfabe += harf

    return ozel_alfabe


def asama1_yerine_koyma(metin, anahtar_kelime, mode='encrypt'):
    standart_alfabe = string.ascii_uppercase
    ozel_alfabe = ozel_alfabe_olustur(anahtar_kelime)

    sonuc = ""
    # Metindeki Türkçe karakterleri temizle
    metin = turkce_karakter_temizle(metin).upper()

    for harf in metin:
        if harf.isalpha():
            if mode == 'encrypt':
                # Standart alfabedeki harfin sırasını bul, özel alfabedeki karşılığını al
                indeks = standart_alfabe.index(harf)
                sonuc += ozel_alfabe[indeks]
            elif mode == 'decrypt':
                # Özel alfabedeki harfin sırasını bul, standart alfabedeki karşılığını al
                indeks = ozel_alfabe.index(harf)
                sonuc += standart_alfabe[indeks]
        else:
            sonuc += harf

    return sonuc


def asama2_blok_yer_degistirme(metin, blok_boyutu=3):
    sonuc = ""
    # Metni baştan sona, blok_boyutu (3) kadar atlayarak tara
    for i in range(0, len(metin), blok_boyutu):
        # 3 karakterlik parçayı al
        blok = metin[i:i + blok_boyutu]
        # Alınan bloğu tersine çevir ([::-1] Python'da stringi ters çevirir) ve sonuca ekle
        sonuc += blok[::-1]

    return sonuc


def asama3_padding_ekle(metin):
    sonuc = ""
    for i in range(len(metin)):
        sonuc += metin[i]
        # Her 2 karakterden sonra 1 rastgele harf ekle
        # i indeksi 0'dan başladığı için (i + 1) % 2 == 0 koşulunu arıyoruz
        if (i + 1) % 2 == 0:
            rastgele_harf = random.choice(string.ascii_uppercase)
            sonuc += rastgele_harf

    return sonuc

def asama3_padding_kaldir(metin):
    sonuc = ""
    for i in range(len(metin)):
        # Eklenen rastgele harfler her 3. karakter konumunda (indeks 2, 5, 8...) olacaktır.
        # Bu yüzden 3'ün katı olan konumları atlayarak orijinal metni geri alıyoruz.
        if (i + 1) % 3 != 0:
            sonuc += metin[i]

    return sonuc

# --- TEST BLOĞU ---
if __name__ == "__main__":
    # Türkçe karakterlerle test ediyoruz
    test_metni = "MÜHENDİS BETÜL"
    anahtar = "ÇAĞDAŞ"

    print(f"Orijinal Metin: {test_metni}\n")

    print(f"Standart Alfabe: {string.ascii_uppercase}")
    print(f"Özel Alfabe    : {ozel_alfabe_olustur(anahtar)}\n")

    # --- ŞİFRELEME (ENCRYPTION) SÜRECİ ---
    adim1_sifreli = asama1_yerine_koyma(test_metni, anahtar, mode='encrypt')
    print(f"Aşama 1 (Yerine Koyma) Sonucu: {adim1_sifreli}")

    adim2_sifreli = asama2_blok_yer_degistirme(adim1_sifreli, blok_boyutu=3)
    print(f"Aşama 2 (Blok Ters Çevirme) Sonucu: {adim2_sifreli}")

    adim3_sifreli = asama3_padding_ekle(adim2_sifreli)
    print(f"Aşama 3 (Dinamik Padding) Sonucu : {adim3_sifreli} \n")

    # --- ŞİFRE ÇÖZME (DECRYPTION) SÜRECİ ---
    print("--- ŞİFRE ÇÖZÜLÜYOR ---")

    # Çözerken işlemleri TAM TERSİ sırayla yapmalıyız: Aşama 3 -> Aşama 2 -> Aşama 1
    adim3_cozulmus = asama3_padding_kaldir(adim3_sifreli)
    adim2_cozulmus = asama2_blok_yer_degistirme(adim3_cozulmus, blok_boyutu=3)
    adim1_cozulmus = asama1_yerine_koyma(adim2_cozulmus, anahtar, mode='decrypt')

    print(f"Tamamen Çözülmüş Metin: {adim1_cozulmus}")