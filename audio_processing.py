import matplotlib.pyplot as plt
import pandas as pd 
from pydub import AudioSegment
from scipy.io import wavfile
import librosa

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

    def get_data(self):
        """Extract MFCC features from WAV files and return sample rates and feature data
        
        Returns:
            tuple: (list of sample rates, list of MFCC feature DataFrames)
        """
        sample_rs = []
        datas = []
        for filename in self.filenames:
            # Load audio file
            data, samrates = librosa.load((self.path + filename + ".wav"), sr=None)

            # Extract MFCC features
            mfccs = librosa.feature.mfcc(y=data, sr=samrates, n_mfcc=15)
            # Convert to DataFrame with labeled columns
            data = pd.DataFrame(mfccs.T, columns=[f"mfcc_{i}" for i in range(1,16)])

            sample_rs.append(samrates)
            datas.append(data)
        return sample_rs, datas



