# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import joblib
import math

# Import sklearn metrics for model evaluation
from sklearn.metrics import classification_report, confusion_matrix

# Import TensorFlow and Keras components
import tensorflow as tf
from tensorflow import keras
from keras._tf_keras.keras.regularizers import l1_l2
from keras._tf_keras.keras import Input, layers
from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.losses import MSE
from keras._tf_keras.keras.models import Sequential, load_model
from keras._tf_keras.keras.layers import (
    SimpleRNN, Dense, Embedding, Masking, LSTM, 
    GRU, Conv1D, Dropout, BatchNormalization, 
    GlobalAveragePooling1D, Flatten
)
from keras._tf_keras.keras.optimizers import Adam
from keras._tf_keras.keras.callbacks import (
    EarlyStopping, 
    ReduceLROnPlateau, 
    ModelCheckpoint
)

class VoiceRecogntion():
    def __init__(self, length, n_features, x_train, y_train) -> None:
        # Initialize model parameters
        self.length = length
        self.n_features = n_features
        self.x_train = x_train
        self.y_train = y_train

        # Set random seeds for reproducibility
        tf.random.set_seed(42)
        np.random.seed(42)

        # Create Sequential model
        self.model = Sequential()
        
        # Define model architecture
        # Input layer
        self.model.add(Input(shape=(n_features, 1), batch_size=32))
        
        # Convolutional layers for feature extraction
        self.model.add(Conv1D(128, 3, padding='same', activation='relu'))
        self.model.add(BatchNormalization())
        self.model.add(Conv1D(64, 3, padding='same', activation='relu'))
        self.model.add(BatchNormalization())
        self.model.add(GlobalAveragePooling1D())
        
        # Dense layers with dropout for regularization
        self.model.add(Dense(1024, activation='relu', kernel_regularizer=l1_l2(l1=0.01, l2=0.01)))
        self.model.add(BatchNormalization())
        self.model.add(Dropout(0.3))  # Increase to 0.3-0.5 range
        
        self.model.add(Dense(512, activation='relu'))
        self.model.add(BatchNormalization())
        self.model.add(Dropout(0.2))
        
        self.model.add(Dense(256, activation='relu'))
        self.model.add(BatchNormalization())
        self.model.add(Dropout(0.1))
        
        # Output layer with softmax activation
        self.model.add(Dense(self.y_train.shape[1], activation='softmax'))

        # Compile model with optimizer and loss function
        self.model.compile(
            loss="mse",
            optimizer=Adam(learning_rate=0.001, clipnorm=1.0),
            metrics=['accuracy']
        )

    def fit_data(self):
        # Define callbacks for training
        callbacks = [
            # Reduce learning rate when validation loss plateaus
            ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5, min_lr=1e-6),
            # Stop training when validation loss stops improving
            EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        ]
        # Train the model
        self.history = self.model.fit(self.x_train, self.y_train,
                               epochs=30,
                               batch_size=32,
                               verbose=1,
                               callbacks=callbacks,
                               validation_split=0.2,
                               shuffle=True)
    
    def prediction(self, x_test, y_test):
        # Make predictions on test data
        y_pred = self.model.predict(x_test, batch_size=32, verbose=1)
        predictions = np.argmax(y_pred, axis=1)
        actual_classes = np.argmax(y_test, axis=1)

        # Calculate confusion matrix
        cm = confusion_matrix(actual_classes, predictions)

        return cm, predictions, actual_classes
    
    def get_score(self, x_test, y_test):
        # Evaluate model performance
        score = self.model.evaluate(x_test, y_test,
                                    batch_size=32,
                                    verbose=1)
        loss = score[0]
        accuracy = score[1]
        return loss, accuracy

    def set_data(self, new_x, new_y):
        # Update training data
        self.x_train = new_x 
        self.y_train = new_y

    def load_model(self):
        # Load saved model from disk
        joblib.load("/Users/sstprk/Desktop/School/CBU/Yazılım Sınama/Proje/Models/model.pkl")
