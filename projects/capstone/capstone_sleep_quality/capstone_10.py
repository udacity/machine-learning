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
import matplotlib.pyplot as plt
import scipy.stats as ss

#Getting preprocessed Data
refined_data = pd.read_csv("first_refined_data.csv")
refined_data = refined_data.drop('Unnamed: 0',axis=1)
pd.set_option("display.max_colwidth", 1000)
pd.set_option("display.max_rows", 1000)


#Getting inputs and outputs
pre_process_obj = pre_process.PreProcess(refined_data,columns_config.columns_config)
pre_process_obj.df, sleep_quality = pre_process_obj.get_inputs_and_outputs()

#Applying one hot encoding
pre_process_obj.apply_one_hot_encoding()



# print pre_process_obj.get_matched_column_names(['99$','98$','97$','96$','94$'])
# sys.exit()
#Dropping unnecessary columns I think this process has to be done in the pre
# pre_process_obj.drop_columns_by_regexp(['99$','98$','97$','96$','94$'])

#Getting final features
features_final = pre_process_obj.df
# print list(features_final)
# sys.exit()


def train_and_test(features_final,target_var):
    # Importing necessary libraries
    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import make_scorer
    from sklearn.cross_validation import train_test_split
    from sklearn.metrics import fbeta_score, accuracy_score
    from sklearn.naive_bayes import GaussianNB
    from sklearn.ensemble import RandomForestClassifier

    from sklearn import tree

    # Splitting the data into training and testing sets
    random_state = 1
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                        target_var,
                                                        test_size=test_size,
                                                        random_state=random_state)

    # Removing outliers
    # from sklearn.neighbors import LocalOutlierFactor
    # outlier_detector = LocalOutlierFactor()
    # detecting_outlier_result = outlier_detector.fit_predict(X_train)
    # index_to_use = np.where(detecting_outlier_result == 1)[0].tolist()
    # X_train = X_train.iloc[index_to_use]
    # y_train = y_train.iloc[index_to_use]

    # Making a base classifier, and finding the best classifier
    base_clf = RandomForestClassifier(random_state=random_state)
    parameters = {'n_estimators': [90, 100, 110, 120, 130, 140, 150, 160, 170,180, 190 ,200]}
    # parameters = {'n_estimators': [100,250, 500, 750,1000]}
    scorer = make_scorer(accuracy_score)
    grid_obj = GridSearchCV(base_clf, parameters, scoring=scorer)
    grid_fit = grid_obj.fit(X_train, y_train)
    best_clf = grid_fit.best_estimator_

    # Getting important features and making it easy to visualize
    base_predictions = (best_clf.fit(X_train, y_train)).predict(X_test)
    feature_importance = pd.Series(data=best_clf.feature_importances_, index=X_train.columns)
    feature_importance.sort_values(ascending=False, inplace=True)

    # Showing the result
    pd.set_option("display.max_colwidth", 1000)
    pd.set_option("display.max_rows", 1000)
    print feature_importance
    print feature_importance[0:99].index.tolist()
    print grid_fit.best_params_
    print "Accuracy on testing data: {:.4f}".format(accuracy_score(y_test, base_predictions))

    return feature_importance


feature_importance = train_and_test(features_final,sleep_quality['q30'])







# features_to_drop = []
# for index,value in feature_importance.iteritems():
#     # print type(important_features)
#     if value < 0.002:
#         features_to_drop.append(index)
# reduced_features_importance = feature_importance.drop(features_to_drop)
# features_to_use = reduced_features_importance.index.tolist()
#
#
# important_features = train_and_test(features_final[features_to_use], sleep_quality['q30'])
#
#






