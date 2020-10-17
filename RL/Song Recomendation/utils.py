import pandas as pd
import datetime
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Util:
    def __init__(self, datapath):
        self.history = []
        self.data, self.song_names = get_data(datapath)
        today = datetime.today()
        start_time = today - relativedelta(minutes=15)
        self.last_listened_times = np.array([np.datetime64(start_time)] * self.data.shape[0])
        self.epsilon = np.array([np.power(2, i) for i in np.arange(0, 16, dtype=float)])
        self.expected_ratings = []

    def add_recommendation(self, song_id):
        self.history.append((song_id, -1))

    def get_number_of_songs(self):
        return self.data.shape[0]

    def get_number_of_features(self):
        return self.data.shape[1]

    def add_rating(self, rating):
        self.history[-1] = (self.history[-1][0], rating)
        song_id = self.history[-1][0]
        self.last_listened_times[song_id] = np.datetime64(datetime.now()) - (
                    np.timedelta64(0, 'ms') + int(np.floor(np.random.rand() * 500)))

    def add_expected_rating(self, rating):
        self.expected_ratings.append(rating)

    def timedelta_to_minute(self, delta):
        return delta.astype('timedelta64[ms]').astype('int')

    def get_history_times(self):
        times = [
            self.timedelta_to_minute(np.datetime64(datetime.now()) - self.last_listened_times[x[0]]) for
            x in self.history]
        return np.array(times)

    def get_features_of_history(self):
        indices = [x[0] for x in self.history]
        return self.data[indices].T

    def get_all_times(self):
        times = [self.timedelta_to_minute(np.datetime64(datetime.now()) - x) for x in
                 self.last_listened_times]
        return np.array(times)

    def get_all_features(self):
        return self.data.T

    def get_all_time_vectors(self):
        return np.array([vectorize(i, self.epsilon) for i in self.get_all_times()]).T

    def get_features_and_times_of_song(self, song_id):
        #print('time', self.timedelta_to_minute(np.datetime64(datetime.now()) - self.last_listened_times[song_id]))
        return self.data[song_id].T, self.timedelta_to_minute(np.datetime64(datetime.now()) - self.last_listened_times[song_id])

    def get_ratings(self):
        return np.array([x[1] for x in self.history])

    def get_features_and_times(self):
        times = self.get_all_times()
        #times_discretized = np.array([vectorize(i, self.epsilon) for i in times])
        concat_data = np.append(self.data, times[:, None], axis=1)
        xmax, xmin = concat_data.max(), concat_data.min()
        return (concat_data - xmin) / (xmax - xmin)

    def get_cumulative_regret(self):
        return (np.absolute(np.array(self.expected_ratings) - np.array([i[1] for i in self.history]))).cumsum()

    def get_cumulative_average_rating(self):
        return np.array([x[1] for x in self.history]).cumsum() / np.arange(1, len(self.history) + 1)


def vectorize(t, epsilon):
    v = np.concatenate([t - epsilon, [t, 1]])
    v[np.where(v < 0)] = 0
    return v

#Function to access the data and preprocess it

def get_data(filepath, separator=';'):
    data = pd.read_csv(filepath, delimiter=separator)
    data.drop(['artist_name_lastfm', "tra_id", "Unnamed: 0", 'title_lastfm', 'track_id'], axis=1, inplace=True)
    data['genre'] = data['genre'].astype('category').cat.codes
    data_x = data.drop(['artist_name', 'title'], axis=1).values
    xmax, xmin = data_x.max(), data_x.min()
    data_x = (data_x - xmin) / (xmax - xmin)
    return data_x, data[['artist_name', 'title']]

#Function to calculate the rating without epsilon-greedy method

def calculate_rating(theta, s, song_features, song_times): 
    return theta.T.dot(song_features) * (1 - np.exp(-song_times / s)) * 10 


#theta,s will be one of the returns you need to get from epsilon-greedy class
# features, times = object_of_the_epsilon_greedy_class.util.get_features_and_times_of_song(recommended_song)
#recommended_song = evaluated using the epsilon-greedy class
