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
labels, features = targetFeatureSplit(data)



### stratified k-fold cross-validation is a form of 
### CV where instances of each class are equally apportioned--
### e.g. if you have 10% of one class and 90% of the other,
### stratification means each fold will have 10% of one
### class and 90% of the other
###
### this is helpful when you don't have a lot of instances
### of one class or the other, because in that case the 
### low-frequency class can become lopsided in the training-test
### split skew the results
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.cross_validation import StratifiedKFold
skf = StratifiedKFold( labels, n_folds=3 )
precisions = []
recalls = []
for train_idx, test_idx in skf: 
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_idx:
        features_train.append( features[ii] )
        labels_train.append( labels[ii] )
    for jj in test_idx:
        features_test.append( features[jj] )
        labels_test.append( labels[jj] )
    
    ### fit the classifier using training set, and test on test set
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)


    ### for each fold, print some metrics
    print
    print "precision score: ", precision_score( labels_test, pred )
    print "recall score: ", recall_score( labels_test, pred )

    precisions.append( precision_score(labels_test, pred) )
    recalls.append( recall_score(labels_test, pred) )

### aggregate precision and recall over all folds
print "average precision: ", sum(precisions)/3.
print "average recall: ", sum(recalls)/3.








#print precision_score( labels_test, pred )
#print recall_score( labels_test, pred )

