import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

from MetinYerleri import *
from GrafikIslemleri import *
from Button import *
from Fonksiyon import *

class SesTanima(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SES TANIMA, SESTEN DUYGU ANALİZİ, KONUŞULAN KONU TAHMİNLEME UYGULAMASI")
        self.setStyleSheet("background-color: #C0E0E0")
        self.setFixedSize(1200, 880)

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
