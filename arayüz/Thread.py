from PyQt5.QtCore import QThread, pyqtSignal


class GeriSayimThread(QThread):
    update_label = pyqtSignal(str)  # Etiketi güncellemek için sinyal oluştur

    def run(self):
        for i in range(3, 0, -1):
            self.update_label.emit(f"{i}")  # Her geri sayım adımında sinyal gönder
            self.sleep(1)  # 1 saniye bekle
        self.update_label.emit("Kayıt başladı!")  # Geri sayım tamamlandığında mesaj
        self.parent().record_from_microphone()  # Kayıt başlat

class BilgilendirmeThread(QThread):
    def __init__(self, parent, message, target):
        super().__init__(parent)
        self.message = message
        self.target = target

    def run(self):
        self.parent().BilgilendirmeKutusu.setText(self.message)
        self.target()