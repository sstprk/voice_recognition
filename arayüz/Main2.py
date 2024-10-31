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
import speech_recognition as sr
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from MetinYerleri import *
from GrafikIslemleri import *
from Button import *

from Fonksiyon import *

class SesTanima(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SES TANIMA, SESTEN DUYGU ANALİZİ, KONUŞULAN KONU TAHMİNLEME UYGULAMASI")
        self.setStyleSheet("background-color: #C0E0E0")
        self.setFixedSize(1200, 800)

        MetinYerleri.MetinYeri(self)
        GrafikIslemleri.GrafikOlustur(self)
        ButonOlustur.GirisMenuButonlari(self)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        SesTanimaSayfasi = SesTanima()
        SesTanimaSayfasi.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Uygulama başlatma hatası: {str(e)}")
