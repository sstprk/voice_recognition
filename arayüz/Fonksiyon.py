from PyQt5.QtWidgets import QWidget, QFileDialog
import sounddevice as sd
from scipy.io.wavfile import write

from GrafikIslemleri import *
from Thread import *
from SesleriAlma import *

class Fonksiyon(QWidget):
    def MikrofondanSesTanima(self):
        try:
            self.bilgilendirme_thread = BilgilendirmeThread(self, "Ses Kaydediliyor.", lambda: SesleriAlma.record_from_mic(self))
            self.bilgilendirme_thread.start()
        except Exception as e:
            print(e)


    def SesDosyasindanSesTanima(self):
        try:
            GrafikIslemleri.clear_graphs(self)
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Ses Dosyası Seç", "", "Ses Dosyaları (*.wav *.mp3)",
                                                       options=options)
            if file_path:
                self.bilgilendirme_thread = BilgilendirmeThread(self, "Lütfen Bekleyiniz, Analiz Ediliyor...",
                    lambda: SesleriAlma.record_from_file(self, file_path))
                self.bilgilendirme_thread.start()
            else:
                self.BilgilendirmeKutusu.setText("Ses dosyası seçilmedi.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(str(e))
