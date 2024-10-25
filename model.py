import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sb

import tensorflow as tf
from tensorflow import keras
from keras._tf_keras.keras import layers
from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.losses import MeanSquaredError
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import SimpleRNN, Dense, Embedding,Masking,LSTM, GRU, Conv1D, Dropout
from keras._tf_keras.keras.optimizers import Adam
from keras._tf_keras.keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler

from keras._tf_keras.keras.preprocessing import sequence
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Dense, Dropout, Embedding, SimpleRNN
from keras._tf_keras.keras.datasets import reuters
from keras._tf_keras.keras.utils import pad_sequences

class VoiceRecogntion():
    def __init__(self, length, n_features, generator) -> None:
        self.length = length
        self.n_features = n_features
        self.generator = generator

        self.model = Sequential()

        self.model.add(LSTM(50, input_shape=(self.length, self.n_features)))
        self.model.add(Dense(1))

        self.model.compile(optimizer="adam", loss="mse")

        self.model.fit(self.generator, epochs=6)