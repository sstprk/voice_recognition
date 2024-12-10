import speech_recognition as Sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import pandas as pd
import numpy as np
from pydub import AudioSegment
import librosa
import os

from GrafikIslemleri import *

class SesIslemleri(QWidget):
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

    def DuyguDurumu(self):
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
            duygu = analyzer.polarity_scores(ceviri_metni)

            self.DuyguDurumu.setText(f"Mutlu: %{duygu['compound'] * 100:.2f}   Mutsuz: %{(1 - duygu['compound']) * 100:.2f}")

        except Exception as e:
            print(e)

    def get_data(self, filename):
        frame_length = 25
        frame_stride = 10
        data, samrates = librosa.load((filename), sr=None)
        data = librosa.util.normalize(data)
        data = librosa.effects.trim(data, top_db=10)
        mfccs = librosa.feature.mfcc(y=data[0], sr=samrates, n_mfcc=128,
                                     hop_length=int(frame_stride * samrates / 1000),
                                     n_fft=int(frame_length * samrates / 1000))

        mfccs = pd.DataFrame(mfccs.T, columns=[f"mfcc_{i}" for i in range(1, 129)])
        np.save("SesTanimaCiktisi", mfccs)

    def load_data(self):
        data = np.load("SesTanimaCiktisi.npy")
        data = np.mean(data, axis=0).reshape(1, -1)
        data_df = pd.DataFrame(data, columns=[f"mfcc_{i}" for i in range(1, data.shape[1] + 1)])
        label = os.path.basename("asd.npy").split(" -")[0]
        data_df['singer'] = label