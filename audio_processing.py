import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
import librosa
from scipy.signal import butter, filtfilt
from sklearn.preprocessing import MinMaxScaler
import os

class AudioProcessor():
    """Audio processing class for converting and extracting features from audio files"""
    
    def __init__(self, path, filenames) -> None:
        """Initialize with path and list of audio filenames"""
        self.path = path
        self.filenames = filenames

    def wav_converter(self, path, filename):
        """Convert a single MP3 file to WAV format"""
        src = path + filename + ".mp3"
        dst = path + filename + ".wav"

        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")

    def to_wav(self):
        """Convert all MP3 files in filenames list to WAV format"""
        for filename in self.filenames:
            self.wav_converter(self.path, filename)

    def split_audio(self, path, filename):
        """Split a single WAV file into 10-second segments"""
        src = path + filename + ".wav"
        dst = path + "Splitted/" + filename + "_"
        sound = AudioSegment.from_wav(src)
        for i in range(0, len(sound), 500):
            split_sound = sound[i:i+1000]
            split_sound.export(dst + str(i) + ".wav", format="wav")

    def get_data(self):
        """Extract MFCC features from WAV files and return sample rates and feature data"""
        
        for filename in self.filenames:
            self.split_audio(self.path, filename)
        
        datas = pd.DataFrame()
        for splitted in os.listdir(self.path + "Splitted/"):
            if splitted.endswith(".wav"):
                # Load audio file
                data, samrates = librosa.load((self.path + "Splitted/" + splitted), sr=None)

                # Extract MFCC features
                mfccs = librosa.feature.mfcc(y=data, sr=samrates, n_mfcc=128)
                data = pd.DataFrame(mfccs.T, columns=[f"mfcc_{i}" for i in range(1,129)])

                np.save(self.path + "MFCC/" + splitted.split(".")[0] + ".npy", data)

    def load_data(self):
        """Load MFCC feature data from files and return a DataFrame
        Returns:
            DataFrame with MFCC features and singer labels
        """
        datas = pd.DataFrame()
        # Process each MFCC feature file
        for fil in os.listdir(self.path + "MFCC/"):
            if fil.endswith(".npy"):
                # Load and reshape data
                data = np.load(self.path + "MFCC/" + fil)
                data = np.mean(data, axis=0).reshape(1,-1)

                # Create DataFrame with MFCC features and singer labels
                data = pd.DataFrame(data, columns=[f"mfcc_{i}" for i in range(1,129)])
                data_y = ["" for x in range(data.shape[0])]
                data_y[data_y == ""] = fil.split(" -")[0]
                data.insert(128, "singer", data_y, True)

                # Append to main DataFrame
                datas = pd.concat([datas, data])
        return datas





