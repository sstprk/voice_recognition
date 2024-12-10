import sounddevice as sd
from scipy.io.wavfile import write

from SesinOzellikIslemleri import *
from GrafikIslemleri import *
import numpy as np
from tensorflow.keras.models import load_model

class Fonksiyon(QWidget):
    def MikrofondanSesTanima(self):
        try:
            GrafikIslemleri.clear_graphs(self)
            self.BilgilendirmeKutusu.setText("Ses Kaydediliyor. Lütfen Bekleyiniz...")
            QApplication.processEvents()
            self.setEnabled(False)

            samplerate = 44100
            duration = 5
            file_path = 'kayit.wav'

            recorded_audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
            sd.wait()

            write(file_path, samplerate, (recorded_audio * 32767).astype(np.int16))

            self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Analiz Ediliyor...")
            QApplication.processEvents()

            SesIslemleri.SestenMetinYapma(self, file_path)

            with open("output.txt", "r", encoding="utf-8") as dosya:
                metin = dosya.read().strip()

            if len(metin) == 0:
                self.BilgilendirmeKutusu.setText("Mikrofon ses alamadı.")
                self.setEnabled(True)
            else:
                self.KacKelimeVar.setText(f"Toplam Sayılan Kelime Sayısı: {len(metin)}")
                Fonksiyon.SarkiSoyleyenBulma(self, file_path)
                SesIslemleri.SesGrafikCiz(self, file_path)
                SesIslemleri.DuyguDurumu(self)
                self.BilgilendirmeKutusu.setText("Mikrofondan ses tanıma tamamlandı.")
                self.setEnabled(True)
        except Exception as e:
            print(e)


    def SesDosyasindanSesTanima(self):
        try:
            GrafikIslemleri.clear_graphs(self)
            self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Ses Dosyası Alınıyor...")
            QApplication.processEvents()
            self.setEnabled(False)

            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Ses Dosyası Seç", "", "Ses Dosyaları (*.wav *.mp3)", options=options)

            self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Analiz Ediliyor...")
            QApplication.processEvents()

            if file_path:
                SesIslemleri.SestenMetinYapma(self, file_path)
                with open("output.txt", "r", encoding="utf-8") as dosya:
                    metin = dosya.read().strip()

                if len(metin) == 0:
                    self.BilgilendirmeKutusu.setText("Ses Dosyasının İçeriği Boştur.")
                    self.setEnabled(True)
                else:
                    self.KacKelimeVar.setText(f"Toplam Sayılan Kelime Sayısı: {len(metin)}")
                    Fonksiyon.SarkiSoyleyenBulma(self, file_path)


                    """test aşamasında spektograma göre duygu analiz kısmı"""
                    """y, sr = librosa.load(file_path)
                    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
                    print(f"Tempo: {tempo} BPM")

                    base_bpm = 120
                    bpm_difference = base_bpm - tempo
                    if bpm_difference > 0:
                        sadness_ratio = min(50 + (bpm_difference * 0.2), 70)
                        happiness_ratio = 100 - sadness_ratio
                    else:
                        happiness_ratio = min(70 + (abs(bpm_difference) * 0.3), 100)
                        sadness_ratio = 100 - happiness_ratio

                    print(f"Mutluluk Oranı: %{happiness_ratio}")
                    print(f"Mutsuzluk Oranı: %{sadness_ratio}")"""

                    SesIslemleri.SesGrafikCiz(self, file_path)
                    SesIslemleri.DuyguDurumu(self)
                    self.BilgilendirmeKutusu.setText("Ses dosyasından ses tanıma tamamlandı.")
                    self.setEnabled(True)
            else:
                self.BilgilendirmeKutusu.setText("Ses dosyası seçilmedi.")
                self.setEnabled(True)
        except Exception as e:
            print(e)


    def SarkiSoyleyenBulma(self, file_path):
        SesIslemleri.get_data(self, file_path)
        SesIslemleri.load_data(self)

        model = load_model("model.keras")
        data = np.load("asd.npy")
        data = data.reshape(1, -1)
        predictions = model.predict(data)
        class_labels = ["Sertab ERENER", "Sezen AKSU", "Yıldız Tilbe"]
        predicted_class_index = np.argmax(predictions)
        predicted_class_label = class_labels[predicted_class_index]

        self.KimKonusuyor.setText(predicted_class_label)