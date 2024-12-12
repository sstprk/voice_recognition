import speech_recognition as Sr
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


from GrafikIslemleri import *
from MetinYerleri import *

class SesIslemleri(QWidget):
    def DuyguDurumuBulma(self):
        try:
            # Metin dosyasını oku
            with open("output.txt", "r", encoding="utf-8") as dosya:
                metin = dosya.read().strip()

            if not metin:
                self.DuyguDurumu.setText("Konuşan Kişinin Duygu Durumu: NÖTR")
                return

            # Çeviri işlemi
            translator = Translator()
            ceviri = translator.translate(metin, src='tr', dest='en')
            ceviri_metni = ceviri.text

            # Duygu analizi
            analyzer = SentimentIntensityAnalyzer()
            self.duygu = analyzer.polarity_scores(ceviri_metni)

            self.DuyguDurumu.setText(f"Mutluluk: %{self.duygu['compound'] * 100:.2f}, Mutsuzluk: %{(1 - self.duygu['compound']) * 100:.2f}")
        except Exception as e:
            print(e)
    def SestenMetinYapma(self, file_path):
        recognizer = Sr.Recognizer()
        try:
            with Sr.AudioFile(file_path) as source:
                audio = recognizer.record(source)

            metin = recognizer.recognize_google(audio, language='tr-TR')
            with open("output.txt", "w", encoding="utf-8") as dosya:
                dosya.write(metin)

        except Sr.UnknownValueError:
            with open("output.txt", "w", encoding="utf-8") as dosya:
                pass
        except Sr.RequestError as e:
            self.BilgilendirmeKutusu.setText(f"Google API'den yanıt alınamadı; {e}")
        except Exception as e:
            print(e)

    def SesGrafikCiz(self, file_path):
        GrafikIslemleri.clear_graphs(self)
        try:
            # Ses dosyasını yükleyerek grafik çizimi
            y, sr = librosa.load(file_path)
            GrafikIslemleri.plot_spectrogram_waveform(self, y, sr)

        except Exception as e:
            print(e)