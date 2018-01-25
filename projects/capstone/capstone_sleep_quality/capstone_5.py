import numpy as np
import pandas as pd
from time import time
from sklearn.model_selection import KFold
import sys
# from sklearn.metrics import r2_score
from sklearn.metrics import fbeta_score, accuracy_score
import math

#import files
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier

import pre_process
import columns_config


refined_data = pd.read_csv("first_refined_data.csv")
refined_data = refined_data.drop('Unnamed: 0',axis=1)

# from sklearn.neighbors import LocalOutlierFactor
# outlier_detector = LocalOutlierFactor()
# detecting_outlier_result = outlier_detector.fit_predict(refined_data)
# index_to_use = np.where(detecting_outlier_result == 1)[0].tolist()
# refined_data = refined_data.loc[index_to_use]

#get inputs and outputs
pre_process_obj = pre_process.PreProcess(refined_data,columns_config.columns_config)

pre_process_obj.df, sleep_quality = pre_process_obj.get_inputs_and_outputs()

#apply one hot encoding
pre_process_obj.apply_one_hot_encoding()

#apply one hot encoding
pre_process_obj.drop_columns_by_regexp(['99$','98$','97$','96$','94$'])

#get final features
features_final = pre_process_obj.df


# import GridSearchCV, make_scorer, train_test_split and metrics
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.cross_validation import train_test_split
from sklearn.metrics import fbeta_score, accuracy_score


# Split the 'features' and 'sleep_quality' data into training and testing sets
random_state = 0
test_size = 0.2
X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                    sleep_quality['q30'],
                                                    test_size = test_size,
                                                    random_state = random_state)

# made a base classifier, and find the best parameters

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
base_clf = RandomForestClassifier()
parameters = {'n_estimators': [70,80,90,100,110,120, 130]}

scorer = make_scorer(accuracy_score)
grid_obj = GridSearchCV(base_clf, parameters, scoring = scorer )
grid_fit = grid_obj.fit(X_train, y_train)
best_clf = grid_fit.best_estimator_

# get feature imortances
base_predictions = (best_clf.fit(X_train, y_train)).predict(X_test)
important_features = pd.Series(data=best_clf.feature_importances_,index=X_train.columns)
important_features.sort_values(ascending=False,inplace=True)

#show the result
print important_features
print important_features[0:99].index.tolist()
print grid_fit.best_params_
print "Accuracy on testing data: {:.4f}".format(accuracy_score(y_test, base_predictions))


#drop unnecessary features
X_train_reduced = X_train[important_features[0:49].index.tolist()]
X_test_reduced = X_test[important_features[0:49].index.tolist()]


# apply adaboost
clf = AdaBoostClassifier(base_estimator = base_clf, random_state = random_state)
parameters = {'n_estimators': [50,75,100], 'learning_rate': [0.15, 0.20,0.25]}
scorer = make_scorer(accuracy_score)
grid_obj = GridSearchCV(clf, parameters, scoring = scorer )
grid_fit = grid_obj.fit(X_train_reduced, y_train)


best_clf = grid_fit.best_estimator_

print grid_fit.best_params_
reduced_predictions = (best_clf.fit(X_train_reduced, y_train)).predict(X_test_reduced)
# best_predictions = best_clf.predict(X_test)

important_features = pd.Series(data=best_clf.feature_importances_,index=X_train_reduced.columns)
important_features.sort_values(ascending=False,inplace=True)
pd.set_option("display.max_colwidth", 1000)

pd.set_option("display.max_rows", 1000)
print important_features
print important_features[0:99].index.tolist()



# print "Final Model trained on full data\n------"
# print "Accuracy on testing data: {:.4f}".format(accuracy_score(y_test, best_predictions))
print "\nFinal Model trained on reduced data\n------"
print "Accuracy on testing data: {:.4f}".format(accuracy_score(y_test, reduced_predictions))



