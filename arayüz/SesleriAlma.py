import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import numpy as np
import librosa
from GrafikIslemleri import *
from MetinYerleri import *
from SestenMetin import *


class SesleriAlma(QWidget):
    def record_from_mic(self):
        try:
            samplerate = 44100  # Hz
            duration = 5  # saniye
            wav_file_path = 'kayit.wav'  # ses kaydı için WAV dosya yolu

            recorded_audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
            sd.wait()

            self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Analiz Ediliyor...")

            write(wav_file_path, samplerate, (recorded_audio * 32767).astype(np.int16))  # örnek genişliğini ayarlama

            y, sr = librosa.load(wav_file_path)
            GrafikIslemleri.plot_spectrogram_waveform(self, y, sr)

            asd.SestenMetinYapma(self, wav_file_path)

            self.BilgilendirmeKutusu.setText("Mikrofondan ses tanıma tamamlandı.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(f"Ses dosyası yükleme hatası: {str(e)}")

    def record_from_file(self, file_path):
        try:
            y, sr = librosa.load(file_path)
            GrafikIslemleri.plot_spectrogram_waveform(self, y, sr)

            # Seçilen dosyadan metin tanıma yap
            asd.SestenMetinYapma(self, file_path)
            self.BilgilendirmeKutusu.setText("Ses dosyasından ses tanıma tamamlandı.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(f"Ses dosyası yükleme hatası: {str(e)}")
