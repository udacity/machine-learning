#!/usr/bin/pickle

""" a basic script for importing student's POI identifier,
    and checking the results that they get from it 
 
    requires that the algorithm, dataset, and features list
    be written to my_classifier.pkl, my_dataset.pkl, and
    my_feature_list.pkl, respectively

    that process should happen at the end of poi_id.py

"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

### load up student's classifier, dataset, and feature_list
clf = pickle.load(open("my_classifier.pkl", "r") )
dataset = pickle.load(open("my_dataset.pkl", "r") )
feature_list = pickle.load(open("my_feature_list.pkl", "r"))

### print basic info about the algorithm/parameters used
print clf

### prepare data for training/testing
data = featureFormat(dataset, feature_list)
features, labels = targetFeatureSplit(data)



### train/test split--randomization in the splitting
### means that rerunning this code multiple times
### will likely give several different precision/recall
### scores below
from sklearn.cross_validation import train_test_split
labels_train, labels_test, features_train, features_test = train_test_split(features, labels, test_size=0.3)



### fit the classifier using training set, and test on test set
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)



### print evaluation metrics
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
print precision_score( labels_test, pred )
print recall_score( labels_test, pred )

