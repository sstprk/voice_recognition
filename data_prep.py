import pandas as pd
import numpy as np

from audio_processing import AudioProcessor
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

class DataPrep():
    def __init__(self, path, filenames, n_ofSingers:int) -> None:
        self.path = path
        self.filenames = filenames
        self.n_ofSingers = n_ofSingers

        self.processor = AudioProcessor(path, filenames)
        self.sample_rates, self.data = self.processor.get_data()

        self.songs_of_each = int(len(self.data) / self.n_ofSingers)

        self.scaled_data = []
        for dat in self.data:
            scaler = MinMaxScaler()
            dat = pd.DataFrame(scaler.fit_transform(dat), columns=dat.columns)
            self.scaled_data.append(dat)

        self.processed_d = self.concat_songs()

        self.train_x, self.test_x, self.train_y, self.test_y = self.prep_data(self.processed_d, test_percent=0.2)

        # Encode labels using OneHotEncoder
        self.encoder = OneHotEncoder(sparse_output=False)
        self.train_y = self.encoder.fit_transform(self.train_y)
        self.test_y = self.encoder.transform(self.test_y)
            

    def feature_selection(self, train_x, train_y):
        """
        Performs feature selection using Random Forest
        Returns feature importance scores
        """
        model = RandomForestClassifier()
        model.fit(train_x, train_y.values.ravel())
        importances = pd.Series(model.feature_importances_, index=train_x.columns)

        return importances.sort_values(ascending=False)
    
    def remove_features(self):
        self.importances = self.feature_selection(self.train_x, self.train_y)
        self.unwanted_features = self.importances[10:len(self.importances)]

        self.train_x = np.array(self.train_x.drop(labels=[x for x in self.unwanted_features.index], axis=1))
        self.test_x = np.array(self.test_x.drop(labels=[x for x in self.unwanted_features.index], axis=1))
    
    def prep_data(self, datast, test_percent):
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
    
    def label_categorical(self, dat, label:int):
        artist = dat
        artist_y = np.zeros(shape=((artist.shape[0]), 1))
        artist_y[artist_y == 0] = label
        artist.insert(15, "singer", artist_y, True)
        return artist
    
    def concat_songs(self):
        artists = []
        i=1
        print(self.scaled_data, self.songs_of_each)
        for i in range(self.songs_of_each+1):
            dat = pd.concat(self.scaled_data[self.songs_of_each*(i-1):self.songs_of_each*i])
            artist = self.label_categorical(dat, i)
            artists.append(artist)
        combined = pd.concat()
        dataset_shuffled = combined.sample(frac=1).reset_index(drop=True)

        return dataset_shuffled
    
    def get_train_data(self):
        return self.train_x, self.train_y
    
    def get_test_data(self):
        return self.test_x, self.test_y

    def get_whole_data(self):
        return pd.concat([self.train_x, self.test_x]), pd.concat([self.train_y, self.test_y])
    
    def get_unwanted(self):
        return self.unwanted_features
    
    def set_unwanted(self, new_unwanted):
        self.unwanted_features = new_unwanted