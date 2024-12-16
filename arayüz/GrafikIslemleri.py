import sys
import librosa
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPalette, QColor
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GrafikIslemleri(QWidget):
    def GrafikOlustur(self):
        # İlk grafik için FigureCanvas oluştur
        self.figure1 = plt.Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setGeometry(20, 140, 1160, 260)  # İlk canvas boyutu ve konumu
        self.canvas1.setParent(self)  # Canvas'ı ana pencereye ekle
        self.canvas1.show()

        # İkinci grafik için FigureCanvas oluştur
        self.figure2 = plt.Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setGeometry(20, 420, 1160, 260)  # İkinci canvas boyutu ve konumu
        self.canvas2.setParent(self)  # Canvas'ı ana pencereye ekle
        self.canvas2.show()

        # İlk başta grafik alanlarını temizle
        self.ax1 = self.figure1.add_subplot(111)  # İlk canvas için ilk subplot
        self.ax2 = self.figure2.add_subplot(111)  # İkinci canvas için ikinci subplot

        #Renk ayarı
        self.figure1.patch.set_facecolor('#C0E0E0')
        self.figure2.patch.set_facecolor('#C0E0E0')

        #Grafik içi renk ayarı
        self.ax1.set_facecolor('#C0E0E0')
        self.ax2.set_facecolor('#C0E0E0')

    def plot_spectrogram_waveform(self, y, sr):
        try:
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