import os
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from Button import *
from MetinYerleri import *
from GrafikOlustur import *
from Thread import *


class SesTanima(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SES TANIMA, SESTEN DUYGU ANALİZİ, KONUŞULAN KONU TAHMİNLEME UYGULAMASI")
        self.setStyleSheet("background-color: #C0E0E0")
        self.setFixedSize(1200, 800)

        ButonOlustur.GirisMenuButonlari(self)
        MetinYerleri.MetinYeri(self)
        GrafikOlustur.GrafikOlustur(self)


    def MikrofondanSesTanima(self):
        try:
            self.clear_graphs()
            self.geri_sayim_thread = GeriSayimThread(self)
            self.geri_sayim_thread.update_label.connect(self.BilgilendirmeKutusu.setText)  # Sinyali bağla
            self.geri_sayim_thread.start()  # Geri sayımı başlat
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)

    def SesDosyasindanSesTanima(self):
        try:
            self.clear_graphs()
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Ses Dosyası Seç", "", "Ses Dosyaları (*.wav *.mp3)",
                                                       options=options)

            if file_path:
                self.bilgilendirme_thread = BilgilendirmeThread(self, "Lütfen Bekleyiniz, Analiz Ediliyor...",
                                                                lambda: self.record_from_file(file_path))
                self.bilgilendirme_thread.start()
            else:
                self.BilgilendirmeKutusu.setText("Ses dosyası seçilmedi.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)

    def clear_graphs(self):
        try:
            # Figürü temizle
            self.figure1.clear()
            self.figure2.clear()

            # Yeni subplotlar oluştur
            self.ax1 = self.figure1.add_subplot(111)  # İlk grafiği ekle
            self.ax2 = self.figure2.add_subplot(111)  # İkinci grafiği ekle

            # Grafik içi renk ayarı
            self.ax1.set_facecolor('#C0E0E0')
            self.ax2.set_facecolor('#C0E0E0')

            # Çizimleri güncelle
            self.canvas1.draw()
            self.canvas2.draw()
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)

    def record_from_microphone(self):
        try:
            duration = 5  # saniye cinsinden ses kaydetme süresi
            sr = 22050  # örnekleme hızı

            # Ses kaydet
            y = sd.rec(int(duration * sr), samplerate=sr, channels=1)
            sd.wait()  # Kayıt bitene kadar bekler
            y = y.flatten()

            # Grafiği çiz
            self.plot_spectrogram_waveform(y, sr)
            self.BilgilendirmeKutusu.setText("Mikrofondan ses tanıma tamamlandı.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)

    def record_from_file(self, file_path):
        try:
            y, sr = librosa.load(file_path)
            self.plot_spectrogram_waveform(y, sr)
            self.BilgilendirmeKutusu.setText("Ses dosyasından ses tanıma tamamlandı.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(f"Ses dosyası yükleme hatası: {e}")

    def plot_spectrogram_waveform(self, y, sr):
        # Mevcut subplot'ları temizle
        self.ax1.clear()
        self.ax2.clear()

        # Dalga formunu ilk canvas üzerinde çiz
        librosa.display.waveshow(y, sr=sr, ax=self.ax1)
        self.ax1.set_title('Dalga Formu')  # Dalga formu için başlık
        self.ax1.set_ylabel('Amplitüd')  # Y ekseni etiketi

        # Spektrogramı hesapla
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

        # Spektrogramı ikinci canvas üzerinde çiz
        librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', cmap='viridis', ax=self.ax2)
        self.ax2.set_title('Spektrogram')  # Spektrogram için başlık
        self.ax2.set_ylabel('Frekans (log)')  # Y ekseni etiketi
        self.figure2.colorbar(self.ax2.collections[0], ax=self.ax2, format='%+2.0f dB')

        # Çizimleri güncelle
        self.canvas1.draw()
        self.canvas2.draw()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        SesTanimaSayfasi = SesTanima()
        SesTanimaSayfasi.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Uygulama başlatma hatası: {e}")
