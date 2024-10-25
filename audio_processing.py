import matplotlib.pyplot as plt
import pandas as pd 
from pydub import AudioSegment
from scipy.io import wavfile

class AudioProcessor():
    def __init__(self, path, filenames) -> None:
        self.path = path
        self.filenames = filenames

    def wav_converter(self, path, filename):
        src = path + filename + ".mp3"
        dst = path + filename + ".wav"

        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")

    def to_wav(self):
        for filename in self.filenames:
            self.wav_converter(self.path, filename)

    def get_data(self):
        sample_rs = []
        datas = []
        for filename in self.filenames:
            samrates, data = wavfile.read((self.path + filename + ".wav"))
            sample_rs.append(samrates)
            datas.append(data)
        return sample_rs, datas



