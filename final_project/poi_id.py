#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat
from feature_format import targetFeatureSplit

### features_list is a list of strings, each of which is a feature name
### first feature must be "poi", as this will be singled out as the label
features_list = ["poi"]


### load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

### we suggest removing any outliers before proceeding further

### if you are creating any new features, you might want to do that here
### store to my_dataset for easy export below
my_dataset = data_dict



### these two lines extract the features specified in features_list
### and extract them from data_dict, returning a numpy array
data = featureFormat(my_dataset, features_list)



### if you are creating new features, could also do that here



### split into labels and features (this line assumes that the first
### feature in the array is the label, which is why "poi" must always
### be first in features_list
labels, features = targetFeatureSplit(data)



### machine learning goes here!
### please name your classifier clf for easy export below

clf = None    ### get rid of this line!  just here to keep code from crashing out-of-box


### dump your classifier, dataset and features_list so 
### anyone can run/check your results
pickle.dump(clf, open("my_classifier.pkl", "w") )
pickle.dump(data_dict, open("my_dataset.pkl", "w") )
pickle.dump(features_list, open("my_feature_list.pkl", "w") )



