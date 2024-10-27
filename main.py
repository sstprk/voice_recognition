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
            "Sertab Erener - Gel Barışalım Artık",
            "Sertab Erener - Lâ'l",
            "Sertab Erener - Yanarım",
            "Yıldız Tilbe - Buz Kırağı",
            "Yıldız Tilbe - Delikanlım",
            "Yıldız Tilbe - Emi"
        ]
    
    # Set path for training audio files
    path = '/Users/sstprk/Desktop/School/CBU/Yazılım Sınama/Proje/Sounds/'
    
    # Initialize audio processor and get data
    processor = AudioProcessor(path, filenames)
    sample_rates, data = processor.get_data()

    # Normalize the data using MinMaxScaler
    for dat in data:
        scaler = MinMaxScaler()
        dat = pd.DataFrame(scaler.fit_transform(dat), columns=dat.columns)

    # Prepare datasets for each artist with labels
    # Artist 1 - Sezen Aksu (Label 1)
    artist1 = pd.concat(data[0:3])
    artist1_y = np.zeros(shape=((artist1.shape[0]), 1))
    artist1_y[artist1_y == 0] = 1
    artist1.insert(15, "singer", artist1_y, True)

    # Artist 2 - Sertab Erener (Label 2)
    artist2 = pd.concat(data[3:6])
    artist2_y = np.zeros(shape=((artist2.shape[0]), 1))
    artist2_y[artist2_y == 0] = 2
    artist2.insert(15, "singer", artist2_y, True)

    # Artist 3 - Yıldız Tilbe (Label 3)
    artist3 = pd.concat(data[6:9])
    artist3_y = np.zeros(shape=((artist3.shape[0]), 1))
    artist3_y[artist3_y == 0] = 3
    artist3.insert(15, "singer", artist3_y, True)

    # Combine all artists' data
    dataset = pd.concat([artist1, pd.concat([artist2, artist3])])

    # Shuffle dataset to prevent overfitting
    dataset_shuffled = dataset.sample(frac=1).reset_index(drop=True)

    # Split data into training and test sets
    train_x, test_x, train_y, test_y = prep_data(dataset, test_percent=0.2)

    # Perform feature selection
    importances = feature_selection(train_x, train_y)
    unwanted_features = importances[10:len(importances)]

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
    Model.load_model()

    # Define test dataset
    test_filenames = [
        "Sezen Aksu - Yalnızca Sitem",
        "Sertab Erener - Yolun Başı",
        "Yıldız Tilbe - Aşkın Benden De Öte"
    ]

    # Process test data
    test_path = '/Users/sstprk/Desktop/School/CBU/Yazılım Sınama/Proje/Sounds/Predict/'
    test_processor = AudioProcessor(test_path, test_filenames)
    test_processor.to_wav()
    test_sample_rates, test_data = test_processor.get_data()

    # Normalize test data
    for dat in test_data:
        scaler = MinMaxScaler()
        dat = pd.DataFrame(scaler.fit_transform(dat), columns=dat.columns)

    # Prepare test datasets for each artist
    # Test Artist 1
    test_artist1 = test_data[0]
    test_artist1_y = np.zeros(shape=((test_artist1.shape[0]), 1))
    test_artist1_y[test_artist1_y == 0] = 1
    test_artist1.insert(15, "singer", test_artist1_y, True)

    # Test Artist 2
    test_artist2 = test_data[1]
    test_artist2_y = np.zeros(shape=((test_artist2.shape[0]), 1))
    test_artist2_y[test_artist2_y == 0] = 2
    test_artist2.insert(15, "singer", test_artist2_y, True)

    # Test Artist 3
    test_artist3 = test_data[2]
    test_artist3_y = np.zeros(shape=((test_artist3.shape[0]), 1))
    test_artist3_y[test_artist3_y == 0] = 3
    test_artist3.insert(15, "singer", test_artist3_y, True)

    # Combine and shuffle test data
    test_dataset = pd.concat([test_artist1, pd.concat([test_artist2, test_artist3])])
    test_dataset_shuffled = test_dataset.sample(frac=1).reset_index(drop=True)

    # Prepare final test data
    test_dataset_y = encoder.transform(pd.DataFrame(test_dataset_shuffled.loc[:, "singer"], columns=["singer"]))
    test_dataset_x = test_dataset_shuffled.drop(labels=["singer"], axis=1)
    test_dataset_x = test_dataset_x.drop(labels=[x for x in unwanted_features.index], axis=1) 

    # Make predictions and get confusion matrix
    confusion_matrix, predictions, actual = Model.prediction(tf.convert_to_tensor(test_dataset_x), tf.convert_to_tensor(test_dataset_y))

    # Visualize results
    plt.figure()
    plt.scatter(actual, predictions)

    # Plot confusion matrix
    plt.figure(figsize=(10, 7))
    sb.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()
