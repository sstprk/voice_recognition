import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import locale

from Fonksiyon import *

class ButonOlustur(QWidget):
    def GirisMenuButonlari(self):
        self.AnaMenuButonlari = []
        self.selected_button = None

        # BUTONLAR OLUŞTURULUYOR
        buttons_info = [
            {"bilgi": "MicrofonSesButton", "text": "MİKROFONDAN SES TANIMA", "position": (120, 20, 420, 40), "function": lambda: Fonksiyon.MikrofondanSesTanima(self)},
            {"bilgi": "DosyadanSesButton", "text": "SES DOSYASINDAN SES TANIMA", "position": (660, 20, 420, 40), "function": lambda: Fonksiyon.SesDosyasindanSesTanima(self)}
        ]

        for button_info in buttons_info:
            bilgi = button_info["bilgi"]
            button = QPushButton(button_info["text"], self)
            button.setGeometry(*button_info["position"])
            button.clicked.connect(button_info["function"])

            #CSS EKLENDİ
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FFA500;
                    border-radius: 20px;
                    color: #333333;
                    font-size: 20px;
                    padding: 0px 0px;
                }
                QPushButton:hover {
                    background-color: #FF8C00;
                }
            """)

            self.AnaMenuButonlari.append(button)
            setattr(self, bilgi, button)
