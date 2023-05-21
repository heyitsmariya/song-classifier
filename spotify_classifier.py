# Load libraries
import sklearn
from sklearn.utils import shuffle
from sklearn import datasets
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style
from sklearn import svm
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing
from matplotlib import pyplot as plt
from pandas import read_csv
from pandas import set_option
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn.metrics import accuracy_score

# Data file import
df = pd.read_csv(r'D:\Users\DELL\Documents\UC\Sem 3\ST\STCapstone\Spotify Classifier Flask\Spotify_Youtube.csv')
df.drop(['Unnamed: 0','Channel','Url_spotify',"Uri","Url_youtube","Title","Views","Likes","Comments","Description","Licensed","official_video"], axis =1, inplace = True)
df.dropna()

# Attribute to be predicted
predict = "Album_type"

#pre-processing
from sklearn.exceptions import DataDimensionalityWarning
#encode object columns to integers
from sklearn import preprocessing
from sklearn.preprocessing import OrdinalEncoder

for col in df:
  if df[col].dtype =='object':
    df[col]=OrdinalEncoder().fit_transform(df[col].values.reshape(-1,1))



#normalize
class_label =df['Album_type']
df = df.drop(['Album_type'], axis =1)
df = (df-df.min())/(df.max()-df.min())
df['Album_type']=class_label


#pre-processing
spotify_data = df.copy()
le = preprocessing.LabelEncoder()
album_type = le.fit_transform((list(spotify_data["Album_type"])))
danceability = le.fit_transform((list(spotify_data["Danceability"])) )
energy = le.fit_transform((list(spotify_data["Energy"])) )
key = le.fit_transform((list(spotify_data["Key"])) )
loudness = le.fit_transform((list(spotify_data["Loudness"])) )
acousticness = le.fit_transform((list(spotify_data["Acousticness"]))  )
instrumentalness = le.fit_transform((list(spotify_data["Instrumentalness"])) )
valence = le.fit_transform((list(spotify_data["Valence"])))


#Predictive model development
x = list(zip( danceability, energy, key , loudness,acousticness, instrumentalness, valence))
y = list(album_type)
# Test options and evaluation metric
num_folds = 5
seed = 7
scoring = 'accuracy'

# Model Test/Train
# Splitting what we are trying to predict into 4 different arrays -
# X train is a section of the x array(attributes) and vise versa for Y(features)
# The test data will test the accuracy of the model created
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.20, random_state=seed)
#splitting 20% of our data into test samples. If we train the model with higher data it already has seen that information and knows

#size of train and test subsets after splitting
print(np.shape(x_train)), print(np.shape(x_test))

# load the model from disk

#Fit with trainining subset
best_model = pickle.load(open('best_model.h5', 'rb'))
y_pred = best_model.predict(x_test)
model_accuracy= accuracy_score(y_test, y_pred)
print("Best Model Accuracy Score on Test Set:", model_accuracy)