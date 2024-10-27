from PyQt5.QtCore import QThread, pyqtSignal

from SesleriAlma import *
from MetinYerleri import *
from GrafikIslemleri import *

class BilgilendirmeThread(QThread):
    def __init__(self, parent, message, target):
        super().__init__(parent)
        self.message = message
        self.target = target

    def run(self):
        try:
            self.parent().BilgilendirmeKutusu.setText(self.message)
            self.target()
        except Exception as e:
            print(f"BilgilendirmeThread içinde bir hata oluştu: {e}")
