import numpy as np
from PyQt5.QtWidgets import QWidget
from tensorflow.keras.models import *
import librosa
import pandas as pd
import os


class SesTanima(QWidget):
    def SarkiSoyleyenBulma(self, file_path):
        SesTanima.SesOzellikCikarma(self, file_path)
        SesTanima.DosyaYukleEtiketle(self)

        model = load_model("model.keras")
        data = np.load("SesTanimaCiktisi.npy")
        data = data.reshape(1, -1)
        predictions = model.predict(data)
        class_labels = ["Sertab ERENER", "Sezen AKSU", "Yıldız Tilbe"]
        predicted_class_index = np.argmax(predictions)
        predicted_class_label = class_labels[predicted_class_index]

        self.KimKonusuyor.setText(predicted_class_label)

    def SesOzellikCikarma(self, filename):
        frame_length = 25
        frame_stride = 10
        data, samrates = librosa.load((filename), sr=None)
        data = librosa.util.normalize(data)
        data = librosa.effects.trim(data, top_db=10)
        mfccs = librosa.feature.mfcc(y=data[0], sr=samrates, n_mfcc=128,
                                     hop_length=int(frame_stride * samrates / 1000),
                                     n_fft=int(frame_length * samrates / 1000))

        mfccs = pd.DataFrame(mfccs.T, columns=[f"mfcc_{i}" for i in range(1, 129)])
        np.save("SesTanimaCiktisi", mfccs)

    def DosyaYukleEtiketle(self):
        data = np.load("SesTanimaCiktisi.npy")
        data = np.mean(data, axis=0).reshape(1, -1)
        data_df = pd.DataFrame(data, columns=[f"mfcc_{i}" for i in range(1, data.shape[1] + 1)])
        label = os.path.basename("asd.npy").split(" -")[0]
        data_df['singer'] = label