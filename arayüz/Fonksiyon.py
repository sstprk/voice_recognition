from PyQt5.QtWidgets import QWidget
import sounddevice as sd
from scipy.io.wavfile import write



from GrafikIslemleri import *
from SesIslemleri import *
from SesTanima import *


class Fonksiyon(QWidget):
    def SesleriAlma(self):
        try:
            clicked_button = self.sender()
            button_name = clicked_button.objectName()

            GrafikIslemleri.clear_graphs(self)

            if button_name == "DosyadanSesButton":
                self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Ses Dosyası Alınıyor...")
                QApplication.processEvents()
                self.setEnabled(False)

                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getOpenFileName(self, "Ses Dosyası Seç", "", "Ses Dosyaları (*.wav *.mp3)",options=options)



            elif button_name == "MikrofonSesButton":
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
                if button_name == "DosyadanSesButton":
                    self.BilgilendirmeKutusu.setText("Ses Dosyasının İçeriği Boştur.")
                elif button_name == "MikrofonSesButton":
                    self.BilgilendirmeKutusu.setText("Mikrofon ses alamadı.")

                self.setEnabled(True)
            else:
                SesTanima.SarkiSoyleyenBulma(self, file_path)
                SesIslemleri.SesGrafikCiz(self, file_path)
                SesIslemleri.DuyguDurumuBulma(self)
                self.KacKelimeVar.setText(f"Toplam Sayılan Kelime Sayısı: {len(metin)}")

                if button_name == "DosyadanSesButton":
                    self.BilgilendirmeKutusu.setText("Ses dosyasından ses tanıma tamamlandı.")
                elif button_name == "MikrofonSesButton":
                    self.BilgilendirmeKutusu.setText("Mikrofondan ses tanıma tamamlandı.")

                self.setEnabled(True)
        except Exception as e:
            print(e)