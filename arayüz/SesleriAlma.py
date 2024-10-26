import sounddevice as sd
from scipy.io.wavfile import write

from GrafikIslemleri import *
from MetinYerleri import *

class SesleriAlma(QWidget):
    def record_from_mic(self):
        try:
            samplerate = 44100  # Hz
            duration = 10  # saniye
            file_path = 'kayit.wav'  # ses kaydı için dosya yolu

            recorded_audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float64')
            sd.wait()  # Kayıt tamamlanana kadar bekle
            self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Analiz Ediliyor...")
            write(file_path, samplerate, recorded_audio)
            y, sr = librosa.load(file_path)
            GrafikIslemleri.plot_spectrogram_waveform(self, y, sr)
            self.BilgilendirmeKutusu.setText("Mikrofondan ses tanıma tamamlandı.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(f"Ses dosyası yükleme hatası: {str(e)}")


    def record_from_file(self, file_path):
        try:
            y, sr = librosa.load(file_path)
            GrafikIslemleri.plot_spectrogram_waveform(self, y, sr)
            self.BilgilendirmeKutusu.setText("Ses dosyasından ses tanıma tamamlandı.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(f"Ses dosyası yükleme hatası: {str(e)}")