import tkinter as tk
from tkinter import ttk, messagebox
import string

# Yazdığımız modülleri içe aktarıyoruz
from klasik_sifreleme import caesar_cipher, vigenere_cipher
from hibrit_algoritma import asama1_yerine_koyma, asama2_blok_yer_degistirme, asama3_padding_ekle, asama3_padding_kaldir
from kriptanaliz import frekans_analizi


class KriptosistemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş Kriptosistem Paneli - Müh. Batool Al-Othman")
        self.root.geometry("750x600")

        # Sekme (Tab) yöneticisini oluştur
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill='both')

        # Sekmeleri (Frame'leri) oluştur
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text='1 - Şifrele')
        self.notebook.add(self.tab2, text='2 - Çöz')
        self.notebook.add(self.tab3, text='3 - Saldırı / Analiz')

        # Sekme İçeriklerini Doldur
        self.sifreleme_sekmesi_olustur()
        self.cozme_sekmesi_olustur()
        self.analiz_sekmesi_olustur()

    # --- SEKME 1: ŞİFRELEME ---
    def sifreleme_sekmesi_olustur(self):
        ttk.Label(self.tab1, text="Şifrelenecek Metin:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.txt_sifrele_girdi = tk.Text(self.tab1, height=5, width=80)
        self.txt_sifrele_girdi.pack(pady=5)

        ayar_frame = ttk.Frame(self.tab1)
        ayar_frame.pack(pady=10)

        ttk.Label(ayar_frame, text="Algoritma:").grid(row=0, column=0, padx=5)
        self.combo_sifrele_algo = ttk.Combobox(ayar_frame, values=["Caesar", "Vigenere", "Özgün Hibrit"])
        self.combo_sifrele_algo.current(2)  # Varsayılan olarak Hibrit seçili
        self.combo_sifrele_algo.grid(row=0, column=1, padx=5)

        ttk.Label(ayar_frame, text="Anahtar / Kaydırma Değeri:").grid(row=0, column=2, padx=5)
        self.entry_sifrele_anahtar = ttk.Entry(ayar_frame)
        self.entry_sifrele_anahtar.grid(row=0, column=3, padx=5)

        ttk.Button(self.tab1, text="Şifrele", command=self.sifrele_calistir).pack(pady=10)

        ttk.Label(self.tab1, text="Şifreli Sonuç:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.txt_sifrele_sonuc = tk.Text(self.tab1, height=10, width=80)
        self.txt_sifrele_sonuc.pack(pady=5)

    def sifrele_calistir(self):
        metin = self.txt_sifrele_girdi.get("1.0", tk.END).strip()
        algo = self.combo_sifrele_algo.get()
        anahtar = self.entry_sifrele_anahtar.get().strip()

        if not metin or not anahtar:
            messagebox.showwarning("Uyarı", "Lütfen metin ve anahtar alanlarını doldurun.")
            return

        sonuc = ""
        try:
            if algo == "Caesar":
                shift = int(anahtar)
                sonuc = caesar_cipher(metin, shift, mode='encrypt')
            elif algo == "Vigenere":
                sonuc = vigenere_cipher(metin, anahtar, mode='encrypt')
            elif algo == "Özgün Hibrit":
                adim1 = asama1_yerine_koyma(metin, anahtar, mode='encrypt')
                adim2 = asama2_blok_yer_degistirme(adim1, blok_boyutu=3)
                sonuc = asama3_padding_ekle(adim2)

            self.txt_sifrele_sonuc.delete("1.0", tk.END)
            self.txt_sifrele_sonuc.insert(tk.END, sonuc)
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {e}")

    # --- SEKME 2: ÇÖZME ---
    def cozme_sekmesi_olustur(self):
        ttk.Label(self.tab2, text="Çözülecek Şifreli Metin:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.txt_coz_girdi = tk.Text(self.tab2, height=5, width=80)
        self.txt_coz_girdi.pack(pady=5)

        ayar_frame = ttk.Frame(self.tab2)
        ayar_frame.pack(pady=10)

        ttk.Label(ayar_frame, text="Algoritma:").grid(row=0, column=0, padx=5)
        self.combo_coz_algo = ttk.Combobox(ayar_frame, values=["Caesar", "Vigenere", "Özgün Hibrit"])
        self.combo_coz_algo.current(2)
        self.combo_coz_algo.grid(row=0, column=1, padx=5)

        ttk.Label(ayar_frame, text="Anahtar / Kaydırma Değeri:").grid(row=0, column=2, padx=5)
        self.entry_coz_anahtar = ttk.Entry(ayar_frame)
        self.entry_coz_anahtar.grid(row=0, column=3, padx=5)

        ttk.Button(self.tab2, text="Şifreyi Çöz", command=self.coz_calistir).pack(pady=10)

        ttk.Label(self.tab2, text="Deşifre Edilmiş Orijinal Metin:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.txt_coz_sonuc = tk.Text(self.tab2, height=10, width=80)
        self.txt_coz_sonuc.pack(pady=5)

    def coz_calistir(self):
        metin = self.txt_coz_girdi.get("1.0", tk.END).strip()
        algo = self.combo_coz_algo.get()
        anahtar = self.entry_coz_anahtar.get().strip()

        if not metin or not anahtar:
            messagebox.showwarning("Uyarı", "Lütfen metin ve anahtar alanlarını doldurun.")
            return

        sonuc = ""
        try:
            if algo == "Caesar":
                shift = int(anahtar)
                sonuc = caesar_cipher(metin, shift, mode='decrypt')
            elif algo == "Vigenere":
                sonuc = vigenere_cipher(metin, anahtar, mode='decrypt')
            elif algo == "Özgün Hibrit":
                adim3 = asama3_padding_kaldir(metin)
                adim2 = asama2_blok_yer_degistirme(adim3, blok_boyutu=3)
                sonuc = asama1_yerine_koyma(adim2, anahtar, mode='decrypt')

            self.txt_coz_sonuc.delete("1.0", tk.END)
            self.txt_coz_sonuc.insert(tk.END, sonuc)
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {e}")

    # --- SEKME 3: ANALİZ / SALDIRI ---
    def analiz_sekmesi_olustur(self):
        ttk.Label(self.tab3, text="Ele Geçirilen Şifreli Metin:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.txt_analiz_girdi = tk.Text(self.tab3, height=4, width=80)
        self.txt_analiz_girdi.pack(pady=5)

        btn_frame = ttk.Frame(self.tab3)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="1. Frekans Analizi Yap", command=self.frekans_calistir).grid(row=0, column=0,
                                                                                                 padx=10)

        ttk.Label(btn_frame, text="Denenecek Anahtarlar\n(Virgülle ayırın):").grid(row=0, column=1, padx=5)
        self.entry_deneme_anahtarlari = ttk.Entry(btn_frame, width=20)
        self.entry_deneme_anahtarlari.grid(row=0, column=2, padx=5)

        ttk.Button(btn_frame, text="2. Anahtarları Dene", command=self.anahtar_deneme_calistir).grid(row=0, column=3,
                                                                                                     padx=10)

        ttk.Label(self.tab3, text="Analiz Sonuçları:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.txt_analiz_sonuc = tk.Text(self.tab3, height=13, width=80)
        self.txt_analiz_sonuc.pack(pady=5)

    def frekans_calistir(self):
        metin = self.txt_analiz_girdi.get("1.0", tk.END).strip()
        if not metin:
            messagebox.showwarning("Uyarı", "Analiz edilecek metni girin.")
            return

        frekanslar = frekans_analizi(metin)

        self.txt_analiz_sonuc.delete("1.0", tk.END)
        self.txt_analiz_sonuc.insert(tk.END, "--- FREKANS ANALİZİ SONUÇLARI ---\n")

        for harf, sayi in frekanslar.items():
            self.txt_analiz_sonuc.insert(tk.END, f"Harf: {harf} -> {sayi} kez geçiyor.\n")

    def anahtar_deneme_calistir(self):
        metin = self.txt_analiz_girdi.get("1.0", tk.END).strip()
        anahtarlar_str = self.entry_deneme_anahtarlari.get().strip()

        if not metin or not anahtarlar_str:
            messagebox.showwarning("Uyarı", "Lütfen şifreli metni ve denenecek anahtarları girin.")
            return

        # Virgülle ayrılmış anahtarları listeye çevir ve boşlukları temizle
        anahtarlar = [a.strip().upper() for a in anahtarlar_str.split(",")]

        self.txt_analiz_sonuc.delete("1.0", tk.END)
        self.txt_analiz_sonuc.insert(tk.END, "--- FARKLI ANAHTARLAR İLE HİBRİT DEŞİFRE DENEMELERİ ---\n\n")

        for anahtar in anahtarlar:
            try:
                # Hibrit sistem deşifre adımları
                cozum3 = asama3_padding_kaldir(metin)
                cozum2 = asama2_blok_yer_degistirme(cozum3, blok_boyutu=3)
                olasi_orijinal_metin = asama1_yerine_koyma(cozum2, anahtar, mode='decrypt')

                self.txt_analiz_sonuc.insert(tk.END, f"Anahtar '{anahtar}' denendi -> Sonuç: {olasi_orijinal_metin}\n")
            except Exception as e:
                self.txt_analiz_sonuc.insert(tk.END, f"Anahtar '{anahtar}' denendi -> (Hata oluştu)\n")


# Bu blok en solda, sıfır girinti ile başlamalıdır.
if __name__ == "__main__":
    root = tk.Tk()
    uygulama = KriptosistemGUI(root)
    root.mainloop()