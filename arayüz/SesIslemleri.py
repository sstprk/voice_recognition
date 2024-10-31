import speech_recognition as Sr
from pydub import AudioSegment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator

from GrafikIslemleri import *
from MetinYerleri import *

class SesIslemleri(QWidget):
    def SestenMetinYapma(self, file_path):
        GrafikIslemleri.clear_graphs(self)

        recognizer = Sr.Recognizer()

        try:
            with Sr.AudioFile(file_path) as source:
                audio = recognizer.record(source)

            y, sr = librosa.load(file_path)
            GrafikIslemleri.plot_spectrogram_waveform(self, y, sr)

            metin = recognizer.recognize_google(audio, language='tr-TR')  # Türkçe için 'tr-TR' kullanılıyor

            # Metin tanımlandıktan sonra hemen dosyaya yazılıyor
            with open("output.txt", "w", encoding="utf-8") as dosya:
                dosya.write(metin)

            self.BilgilendirmeKutusu.setText("Metin başarıyla kaydedildi. Grafikler Çiziliyor...")
        except Sr.UnknownValueError:
            self.BilgilendirmeKutusu.setText("Ses tanınamadı.")
        except Sr.RequestError as e:
            self.BilgilendirmeKutusu.setText(f"Google API'den yanıt alınamadı; {e}")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(f"Bir hata oluştu: {e}")

    def DuyguDurumu(self):
        try:
            with open("output.txt", "r", encoding="utf-8") as dosya:
                metin = dosya.read()

            # Çeviri işlemi
            translator = Translator()
            ceviri = translator.translate(metin, src='tr', dest='en')

            # Çevrilen metni al
            ceviri_metni = ceviri.text

            # Duygu analizi yap
            analyzer = SentimentIntensityAnalyzer()
            duygu = analyzer.polarity_scores(ceviri_metni)

            # Duygu durumu kontrolü
            if duygu['compound'] >= 0.05:
                self.DuyguDurumu.setText("Konuşan Kişinin Duygu Durumu: Olumlu")
            elif duygu['compound'] <= -0.05:
                self.DuyguDurumu.setText("Konuşan Kişinin Duygu Durumu: Olumsuz")
            else:
                self.DuyguDurumu.setText("Konuşan Kişinin Duygu Durumu: Nötr")
        except Exception as e:
            print(e)