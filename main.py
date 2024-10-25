import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sb

from model import VoiceRecogntion
from audio_processing import AudioProcessor

filenames = [
        "Sezen Aksu - İki Gözüm",
        "Sezen Aksu - Küçüğüm",
        "Sezen Aksu - Sen Ağlama"
    ]
    
path = '/Users/sstprk/Desktop/School/CBU/Yazılım Sınama/Proje/Sounds/'

processor = AudioProcessor(path, filenames)
sample_rates, data = processor.get_data()

song1 = pd.DataFrame(data[0], columns=["Left", "Right"])
song2 = pd.DataFrame(data[1], columns=["Left", "Right"])
song3 = pd.DataFrame(data[2], columns=["Left", "Right"])

#SET THE MODEL PARAMETERS AND TRY THE DATA WİTH THE MODEL!!!!!!

print(song1)
print(song2.shape)
print(song3.shape)

plt.figure(0)
plt.plot(song1["Left"])

plt.figure(1)
plt.plot(song2["Left"])

plt.figure(2)
plt.plot(song3["Left"])
plt.show()