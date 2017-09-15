from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import sys
classifier = LinearRegression()
data = pd.read_csv("data.csv")
# TODO: Separate the features and the labels into arrays called X and y
X = np.array(data[['x1', 'x2']])
y = np.array(data['y'])
print data
sys.exit()
classifier.fit(X,y)
guesses = classifier.predict(X)
# guesses = mean_absolute_error(y,guesses)
# print guesses
sys.exit()