import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPalette, QColor

class MetinYerleri(QWidget):
    def MetinYeri(self):
        self.labels = []

        # UYARI-BİLGİLENDİRME MESAJ YERLERİ OLUŞTURULDU
        labels_info = [
            {"bilgi": "BilgilendirmeKutusu", "text": "Lütfen bir seçim yapınız.", "position": (0, 80, 1200, 40)},
            {"bilgi": "KimKonusuyor", "text": "", "position": (0, 680, 1200, 40)},
            {"bilgi": "DuyguDurumu", "text": "", "position": (0, 740, 1200, 40)},
            {"bilgi": "KacKelimeVar", "text": "", "position": (0, 800, 1200, 40)},
        ]

        for label_info in labels_info:
            bilgi = label_info["bilgi"]
            label = QLabel(label_info["text"], self)
            label.setGeometry(*label_info["position"])

            label.show()

            # CSS EKLENDİ
            label.setStyleSheet("""
                QLabel {
                    color: #333333;
                    font-family: "Arial", sans-serif; /* Yazı fontu */
                    font-size: 30px;
                }
            """)

            label.setAlignment(Qt.AlignCenter)

            self.labels.append(label)
            setattr(self, bilgi, label)