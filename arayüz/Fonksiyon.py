from PyQt5.QtWidgets import QWidget
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import io


import speech_recognition as sr
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords


from GrafikIslemleri import *
from SesIslemleri import *
from SesTanima import *


class Fonksiyon(QWidget):
    def AnaIslemler(self):
        try:
            clicked_button = self.sender()
            button_name = clicked_button.objectName()
            GrafikIslemleri.clear_graphs(self)

            file_path = Fonksiyon.SesleriAlma(self, button_name)

            if file_path == 404:
                self.BilgilendirmeKutusu.setText("Dosya alınamadı.")
                return

            self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Analiz Ediliyor...")
            QApplication.processEvents()

            SesIslemleri.SestenMetinYapma(self, file_path)

            Fonksiyon.SesleriAnalizEtme(self, button_name, file_path)
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)

    def SesleriAlma(self, button_name):
        try:
            if button_name == "DosyadanSesButton":
                self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Ses Dosyası Alınıyor...")
                QApplication.processEvents()

                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getOpenFileName(self, "Ses Dosyası Seç", "", "Ses Dosyaları (*.wav *.mp3)",
                                                           options=options)

            elif button_name == "MikrofonSesButton":
                self.BilgilendirmeKutusu.setText("Ses Kaydediliyor. Lütfen Bekleyiniz...")
                QApplication.processEvents()

                samplerate = 44100
                duration = 5
                file_path = 'kayit.wav'

                recorded_audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
                sd.wait()

                write(file_path, samplerate, (recorded_audio * 32767).astype(np.int16))

            if file_path:
                return file_path
            else:
                return 404
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)

    def SesleriAnalizEtme(self, button_name, file_path):
        try:
            with open("output.txt", "r", encoding="utf-8") as dosya:
                metin = dosya.read().strip()

            if len(metin) == 0:
                if button_name == "DosyadanSesButton":
                    self.BilgilendirmeKutusu.setText("Ses Dosyasının İçeriği Boştur.")
                elif button_name == "MikrofonSesButton":
                    self.BilgilendirmeKutusu.setText("Konuşma bulunmamaktadır.")
            else:
                SesTanima.SarkiSoyleyenBulma(self, file_path)
                SesIslemleri.SesGrafikCiz(self, file_path)
                SesIslemleri.DuyguDurumuBulma(self)
                self.KacKelimeVar.setText(f"Toplam Sayılan Kelime Sayısı: {len(metin)}")

                if button_name == "DosyadanSesButton":
                    self.BilgilendirmeKutusu.setText("Ses dosyasından ses tanıma tamamlandı.")
                elif button_name == "MikrofonSesButton":
                    self.BilgilendirmeKutusu.setText("Mikrofondan ses tanıma tamamlandı.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)