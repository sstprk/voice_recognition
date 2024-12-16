import threading

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt


from Fonksiyon import *

class Thread(QWidget):
    def Thread(self):
        thread = threading.Thread(target=Fonksiyon.AnaIslemler(self))
        thread.start()