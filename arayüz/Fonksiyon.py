import sounddevice as sd
from scipy.io.wavfile import write

from SesinOzellikIslemleri import *
from GrafikIslemleri import *

class Fonksiyon(QWidget):
    def MikrofondanSesTanima(self):
        try:
            GrafikIslemleri.clear_graphs(self)
            self.BilgilendirmeKutusu.setText("Ses Kaydediliyor. Lütfen Bekleyiniz...")
            QApplication.processEvents()
            self.setEnabled(False)

            samplerate = 44100
            duration = 5
            wav_file_path = 'kayit.wav'

            recorded_audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
            sd.wait()

            write(wav_file_path, samplerate, (recorded_audio * 32767).astype(np.int16))

            self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Analiz Ediliyor...")
            QApplication.processEvents()

            SesIslemleri.SestenMetinYapma(self, wav_file_path)
            SesIslemleri.DuyguDurumu(self)
            self.setEnabled(True)

            self.BilgilendirmeKutusu.setText("Mikrofondan ses tanıma tamamlandı.")
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
                SesIslemleri.DuyguDurumu(self)

                self.setEnabled(True)
                self.BilgilendirmeKutusu.setText("Ses dosyasından ses tanıma tamamlandı.")
            else:
                self.BilgilendirmeKutusu.setText("Ses dosyası seçilmedi.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(str(e))