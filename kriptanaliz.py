def frekans_analizi(metin):
    """
    Şifreli metindeki harflerin kaç kez geçtiğini sayar
    ve en çok kullanılandan en aza doğru sıralar.
    """
    frekanslar = {}

    # Sadece harfleri say (boşluk veya noktalama işaretlerini yoksay)
    for harf in metin.upper():
        if harf.isalpha():
            if harf in frekanslar:
                frekanslar[harf] += 1
            else:
                frekanslar[harf] = 1

    # Sözlüğü değerlerine (geçme sayılarına) göre büyükten küçüğe sırala
    sirali_frekans = dict(sorted(frekanslar.items(), key=lambda item: item[1], reverse=True))

    return sirali_frekans


def harf_sayimini_yazdir(frekans_sozlugu):
    """
    Sıralanmış frekans sözlüğünü ekrana düzgün bir formatta yazdırır.
    """
    print("--- FREKANS ANALİZİ SONUÇLARI ---")
    for harf, sayi in frekans_sozlugu.items():
        print(f"Harf: {harf} -> {sayi} kez kullanılmış")
    print("-" * 32)


# Test bloğu
if __name__ == "__main__":
    # Test için diğer dosyamızdan fonksiyonları içe aktarıyoruz
    from hibrit_algoritma import asama1_yerine_koyma, asama2_blok_yer_degistirme, asama3_padding_ekle

    orijinal_metin = "KRIPTOLOJI PROJESI "
    gercek_anahtar = "MÜDENDIS"

    print(f"Orijinal Metin: {orijinal_metin}")

    # --- Hedef Şifreli Metni Oluşturalım ---
    adim1 = asama1_yerine_koyma(orijinal_metin, gercek_anahtar, mode='encrypt')
    adim2 = asama2_blok_yer_degistirme(adim1, blok_boyutu=3)
    ele_gecirilen_sifreli_metin = asama3_padding_ekle(adim2)

    print(f"\nEle Geçirilen Şifreli Metin:\n{ele_gecirilen_sifreli_metin}\n")

    # --- 1. SALDIRI: FREKANS ANALİZİ ---
    frekanslar = frekans_analizi(ele_gecirilen_sifreli_metin)
    harf_sayimini_yazdir(frekanslar)

    # --- 2. SALDIRI: FARKLI ANAHTARLAR DENEME ---
    print("\n--- FARKLI ANAHTARLAR İLE ŞİFRE ÇÖZME DENEMELERİ ---")
    denenecek_anahtarlar = ["ELMA", "PROJE", "MUDENDIS", "PYTHON"]

    from hibrit_algoritma import asama3_padding_kaldir

    for deneme_anahtari in denenecek_anahtarlar:
        # Şifreyi bu deneme anahtarıyla çözmeye çalışıyoruz
        cozum3 = asama3_padding_kaldir(ele_gecirilen_sifreli_metin)
        cozum2 = asama2_blok_yer_degistirme(cozum3, blok_boyutu=3)
        olasi_orijinal_metin = asama1_yerine_koyma(cozum2, deneme_anahtari, mode='decrypt')

        print(f"Anahtar '{deneme_anahtari}' deneniyor -> Sonuç: {olasi_orijinal_metin}")