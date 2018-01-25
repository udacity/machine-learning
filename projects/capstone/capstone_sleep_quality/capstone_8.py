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

#remove outliers
# from sklearn.neighbors import LocalOutlierFactor
# outlier_detector = LocalOutlierFactor()
# detecting_outlier_result = outlier_detector.fit_predict(refined_data)
# index_to_use = np.where(detecting_outlier_result == 1)[0].tolist()
# refined_data = refined_data.loc[index_to_use]

#get inputs and outputs
pre_process_obj = pre_process.PreProcess(refined_data,columns_config.columns_config)

pre_process_obj.df, sleep_quality = pre_process_obj.get_inputs_and_outputs()

# sleep_quality = sleep_quality.apply(lambda x: 1 if 'q30' <= 2 else 0 )
# print sleep_quality

# make a target variable to binary classification
for key,value in sleep_quality.iterrows():
    # print v1
    if value['q30'] <= 2:
        value['q30'] = 1
    else:
        value['q30'] = 0

# print sleep_quality
# sys.exit()
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
from sklearn.ensemble import IsolationForest
from sklearn import tree
from sklearn.neighbors import LocalOutlierFactor


base_clf = RandomForestClassifier(random_state = random_state)

# base_clf = tree.DecisionTreeClassifier()
# base_clf = GaussianNB()
parameters = {'n_estimators': [70,80,90,100,110,120, 130]}

scorer = make_scorer(accuracy_score)
grid_obj = GridSearchCV(base_clf, parameters, scoring = scorer )
grid_fit = grid_obj.fit(X_train, y_train)
best_clf = grid_fit.best_estimator_
# best_clf = base_clf

# get feature imortances
base_predictions = (best_clf.fit(X_train, y_train)).predict(X_test)
important_features = pd.Series(data=best_clf.feature_importances_,index=X_train.columns)
important_features.sort_values(ascending=False,inplace=True)

#show the result
print important_features
# print important_features[0:99].index.tolist()
print grid_fit.best_params_
print "Accuracy on testing data: {:.4f}".format(accuracy_score(y_test, base_predictions))

# print important_features[0]
# print type(important_features)
# print len(base_predictions)
# print type(base_predictions)
features_final['q30'] = sleep_quality['q30']
# print refined_data['q30']
# sys.exit()

# X_test['having_good_sleep'] = base_predictions
pd.set_option("display.max_colwidth", 1000)
pd.set_option("display.max_rows", 1000)
# print X_test['having_good_sleep']

features_to_focus = list(important_features[0:99].index)
# predicted_sleep_quality = pd.DataFrame(data=base_predictions,columns=['having_good_sleep'])
# print predicted_sleep_quality
# print features_to_focus
# print type(features_to_focus)
# sys.exit()
# print X_test[['q19a_4']]
# sys.exit()
correlations =  features_final.corr().filter(features_to_focus).drop(features_to_focus)
print correlations.iloc[-1].sort_values(ascending=False)
# print correlations.iloc[-1].sort_values(ascending=False)
# print type(correlations.iloc[-1])
# print list(important_features[0:99].index)
# print refined_data.corr().filter(important_features[0:1]).drop()
