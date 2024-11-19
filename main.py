# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

# Import machine learning related libraries
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from keras._tf_keras.keras.preprocessing.sequence import TimeseriesGenerator
from model import VoiceRecogntion
from audio_processing import AudioProcessor
import tensorflow as tf

def get_data(path, filenames):
    """
    Gets data from audio files
    Args:
        path: Path to audio files
        filenames: List of audio filenames
    Returns:
        Cleaned dataset
    """
    audio_processor = AudioProcessor(path, filenames)
    audio_processor.get_data()
    datas = audio_processor.load_data()
    return datas

def prep_data(datast, test_percent):
    """
    Prepares training and test datasets
    Args:
        datast: Input dataset
        test_percent: Percentage of data to be used for testing
    Returns:
        Training and test splits for features and labels
    """
    data_y = datast.loc[:,"singer"]
    data_x = datast.drop("singer", axis=1)
    
    test_point = np.round(len(data_x)*test_percent)
    test_ind = int(len(data_x)-test_point)

    x_train = data_x.iloc[:test_ind]
    x_test = data_x.iloc[test_ind:]   

    y_train = pd.DataFrame(data_y.iloc[:test_ind], columns=["singer"])
    y_test = pd.DataFrame(data_y.iloc[test_ind:], columns=["singer"])

    return x_train, x_test, y_train, y_test

def feature_selection(train_x, train_y):
    """
    Performs feature selection using Random Forest
    Returns feature importance scores
    """
    model = RandomForestClassifier()
    model.fit(train_x, train_y.values.ravel())
    importances = pd.Series(model.feature_importances_, index=train_x.columns)

    return importances.sort_values(ascending=False)

if __name__ == "__main__":
    # Define training dataset song files
    filenames = [
            "Sezen Aksu - İki Gözüm",
            "Sezen Aksu - Küçüğüm",
            "Sezen Aksu - Sen Ağlama",
            "Sezen Aksu - Son Bakış",
            "Sezen Aksu - Beni Unutma",
            "Sezen Aksu - Gülümse",
            "Sertab Erener - Gel Barışalım Artık",
            "Sertab Erener - Lâ'l",
            "Sertab Erener - Yanarım",
            "Sertab Erener - Olsun",
            "Sertab Erener - Rüya",
            "Sertab Erener - Vur Yüreğim",
            "Yıldız Tilbe - El Adamı",
            "Yıldız Tilbe - Sevmeyeceğim",
            "Yıldız Tilbe - Vazgeçtim",
            "Yıldız Tilbe - Buz Kırağı",
            "Yıldız Tilbe - Delikanlım",
            "Yıldız Tilbe - Emi"
        ]
    
    # Set path for training audio files
    path = '/Users/sstprk/Desktop/School/CBU/Yazılım Sınama/Proje/Sounds/Turkish Songs/Train/'
    
    # Initialize audio processor and get data
    data = get_data(path=path, filenames=filenames)

    # Shuffle dataset to prevent overfitting
    dataset_shuffled = data.sample(frac=1).reset_index(drop=True)

    # Split data into training and test sets
    train_x, test_x, train_y, test_y = prep_data(data, test_percent=0.2)

    # Perform feature selection
    importances = feature_selection(train_x, train_y)
    unwanted_features = importances[28:len(importances)]

    # Remove less important features
    train_x = np.array(train_x.drop(labels=[x for x in unwanted_features.index], axis=1))
    test_x = np.array(test_x.drop(labels=[x for x in unwanted_features.index], axis=1))

    # Encode labels using OneHotEncoder
    encoder = OneHotEncoder(sparse_output=False)
    train_y = encoder.fit_transform(train_y)
    test_y = encoder.transform(test_y)

    # Get model dimensions
    n_features = train_x.shape[1]
    length = train_x.shape[0]

    # Initialize and load the model
    Model = VoiceRecogntion(length=length, n_features=n_features, x_train=train_x, y_train=train_y)
    Model.fit_data()
    #Model.load_model()

    Model.get_score(test_x, test_y)

    # Define test dataset
    test_filenames = [
        "Sezen Aksu - Yalnızca Sitem",
        "Sertab Erener - Yolun Başı",
        "Yıldız Tilbe - Aşkın Benden De Öte"
    ]

    # Process test data
    test_path = '/Users/sstprk/Desktop/School/CBU/Yazılım Sınama/Proje/Sounds/Turkish Songs/Predict/'
    test_data = get_data(test_path, test_filenames)

    test_dataset_shuffled = test_data.sample(frac=1).reset_index(drop=True)

    # Prepare final test data
    test_dataset_y = encoder.transform(pd.DataFrame(test_dataset_shuffled.loc[:, "singer"], columns=["singer"]))
    test_dataset_x = test_dataset_shuffled.drop(labels=["singer"], axis=1)
    test_dataset_x = test_dataset_x.drop(labels=[x for x in unwanted_features.index], axis=1) 

    # Make predictions and get confusion matrix
    confusion_matrix, predictions, actual = Model.prediction(tf.convert_to_tensor(test_dataset_x), tf.convert_to_tensor(test_dataset_y))

    # Plot confusion matrix
    plt.figure(figsize=(10, 7))
    sb.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()
