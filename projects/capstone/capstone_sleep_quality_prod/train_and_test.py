# Importing necessary processes
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import fbeta_score, accuracy_score
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
import numpy as np
import pandas as pd
import sys
from lib import pre_process
import columns_config
import time
current_module = sys.modules[__name__]

# Loading first-preprocessed data
def get_feature_final_and_target_var(benchmark=False):

    if benchmark == True:
        refined_data = pd.read_csv("first_refined_csv_for_benchmark.csv")
    else:
        refined_data = pd.read_csv("first_refined_data.csv")
    refined_data = refined_data.drop('Unnamed: 0',axis=1)
    pd.set_option("display.max_colwidth", 1000)
    pd.set_option("display.max_rows", 1000)

    # Getting inputs and outputs
    pre_process_obj = pre_process.PreProcess(refined_data,columns_config.columns_config)

    # Dividing input and output variables
    pre_process_obj.df, sleep_quality = pre_process_obj.get_inputs_and_outputs()

    # Applying one hot encoding
    pre_process_obj.apply_one_hot_encoding()

    # Getting final features
    features_final = pre_process_obj.df

    return features_final,sleep_quality['q30']

def initial_train_and_measure_performance(random_state,features_final,target_var):

    # Getting start time of this process
    start_time = time.time()

    result = {}

    # Storing current random_state to the result
    result['random_state'] = random_state

    # Splitting the 'features' and 'sleep_quality' data into training and testing sets
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                        target_var,
                                                        test_size=test_size,
                                                        random_state=random_state)

    # Removing outliers
    outlier_detector = LocalOutlierFactor()  # Creating the object of LocalOutlierFactor
    detecting_outlier_result = outlier_detector.fit_predict(X_train)  # Getting the outliers and non-outliers

    # Extracting the indexes of non-outliers
    index_to_use = np.where(detecting_outlier_result == 1)[0].tolist()

    # Removing outliers from the training dataset
    X_train = X_train.iloc[index_to_use]
    y_train = y_train.iloc[index_to_use]


    # Making a base classifier (RandomForest)
    base_clf = RandomForestClassifier(random_state=random_state)

    # Making a model by training dataset and predictions
    base_predictions = base_clf.fit(X_train, y_train).predict(X_test)

    # Measuring the F1 score of the predictions of the base classifier
    base_clf_f1_score = fbeta_score(y_test, base_predictions,1,average="macro")

    # Storing the F1 score of the base classifier
    result['base_clf_f1_score'] = base_clf_f1_score

    # Showing the F1 score of base classifier
    print "F1 score of base clf on testing data: {:.4f}".format(base_clf_f1_score)

    # Making AdaBoosted Random Forest
    clf = AdaBoostClassifier(base_estimator=base_clf, random_state=random_state)
    predictions = clf.fit(X_train, y_train).predict(X_test)
    f1_score = fbeta_score(y_test, predictions,1, average="macro")

    # Storing the F1 score of the boosted classifier
    result['boosted_clf_f1_score'] = f1_score

    # Showing the F1 score of the boosted classifier and the time took for executing entire process
    print "F1 score of boosted clf on testing data: {:.4f}".format(f1_score)
    print("--- %s seconds ---" % (time.time() - start_time))
    return result


def train_and_measure_performance_1(random_state,features_final,target_var,f_select_range):

    # Getting start time of this process
    start_time = time.time()

    result = {}

    # Storing current random_state to the result
    result['random_state'] = random_state

    # Splitting the 'features' and 'sleep_quality' data into training and testing sets
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                        target_var,
                                                        test_size=test_size,
                                                        random_state=random_state)

    # Removing outliers
    outlier_detector = LocalOutlierFactor()  # Creating the object of LocalOutlierFactor
    detecting_outlier_result = outlier_detector.fit_predict(X_train)  # Getting the outliers and non-outliers

    # Extracting the indexes of non-outliers
    index_to_use = np.where(detecting_outlier_result == 1)[0].tolist()

    # Removing outliers from the training dataset
    X_train = X_train.iloc[index_to_use]
    y_train = y_train.iloc[index_to_use]


    # Making a base classifier (RandomForest)
    clf = RandomForestClassifier(random_state=random_state)

    # Finding the best parameter and classifier by GridSearch
    parameters = {
        'n_estimators': [10,50,100,200,300,400,500]}  # As far as I try, selecting parameters from these values performs well
    scorer = make_scorer(fbeta_score,beta=1,average="macro")
    grid_obj = GridSearchCV(clf, parameters, scoring=scorer)
    grid_fit = grid_obj.fit(X_train, y_train)
    base_clf = grid_fit.best_estimator_

    # Train with training dataset and make predictions
    base_predictions = (base_clf.fit(X_train, y_train)).predict(X_test)

    # Getting feature importance and sorting them in descending order
    important_features = pd.Series(data=base_clf.feature_importances_, index=X_train.columns)
    important_features.sort_values(ascending=False, inplace=True)

    # Measuring the F1 score of the predictions of the base classifier
    base_clf_fbeta_score = fbeta_score(y_test, base_predictions,beta=1,average="macro")

    # Getting its best parameters
    base_clf_params = grid_fit.best_params_

    # Showing the best parameters of the base classifier
    print base_clf_params
    print "F1 score on testing data: {:.4f}".format(base_clf_fbeta_score)

    # Storing the F1 score of the best base classifier and its best parameter
    result['base_clf_f1_score'] = base_clf_fbeta_score
    result['base_clf_n_estimators'] = base_clf_params['n_estimators']



    # Dropping less important features
    if f_select_range:
        X_train_reduced = X_train[important_features[f_select_range[0]:f_select_range[1]].index.tolist()]
        X_test_reduced = X_test[important_features[f_select_range[0]:f_select_range[1]].index.tolist()]
    else:
        X_train_reduced = X_train
        X_test_reduced = X_test



    # Making AdaBoost classifier from the base classifier, then applying grid search
    clf = AdaBoostClassifier(base_estimator=base_clf, random_state=random_state)
    parameters = {'n_estimators': [10, 25, 50], 'learning_rate': [0.05, 0.1, 0.15]}
    scorer = make_scorer(fbeta_score,beta=1,average="macro")
    grid_obj = GridSearchCV(clf, parameters, scoring=scorer)
    grid_fit = grid_obj.fit(X_train_reduced, y_train)
    best_clf = grid_fit.best_estimator_

    # Train the best clf with reduced training set
    reduced_predictions = (best_clf.fit(X_train_reduced, y_train)).predict(X_test_reduced)

    # Getting feature importance and sorting them in descending order
    important_features = pd.Series(data=best_clf.feature_importances_, index=X_train_reduced.columns)
    important_features.sort_values(ascending=False, inplace=True)

    # Getting best parameters of the best boosted classifier
    best_clf_params = grid_fit.best_params_

    # Measuring the F1 score of the predictions of the best boosted classifier
    best_clf_fbeta_score = fbeta_score(y_test, reduced_predictions,1,average='macro')

    # Storing each result
    result['best_clf_f1_score'] = best_clf_fbeta_score
    result['best_clf_n_estimators'] = best_clf_params['n_estimators']
    result['best_clf_learning_rate'] = best_clf_params['learning_rate']
    result['time'] = (time.time() - start_time)

    # Showin each result
    print best_clf_params
    print "\nFinal Model trained on reduced data\n------"
    print "F1 score on testing data: {:.4f}".format(best_clf_fbeta_score)
    print("--- %s seconds ---" % result['time'])
    return result

def train_and_measure_performance_2(random_state,features_final,target_var,f_select_range,base_clf_n_estimators,boosting_clf_n_estimators,boosting_clf_learning_rate ):

    # Getting start time of this process
    start_time = time.time()

    result = {}

    # Storing current random_state to the result
    result['random_state'] = random_state

    # Splitting the 'features' and 'sleep_quality' data into training and testing sets
    # random_state = 1
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                        target_var,
                                                        test_size=test_size,
                                                        random_state=random_state)

    # Removing outliers
    outlier_detector = LocalOutlierFactor()  # Creating the object of LocalOutlierFactor
    detecting_outlier_result = outlier_detector.fit_predict(X_train)  # Getting the outliers and non-outliers

    # Extracting the indexes of non-outliers
    index_to_use = np.where(detecting_outlier_result == 1)[0].tolist()

    # Removing outliers from the training dataset
    X_train = X_train.iloc[index_to_use]
    y_train = y_train.iloc[index_to_use]


    # Making a base classifier (RandomForest) with best parameters
    base_clf = RandomForestClassifier(n_estimators=base_clf_n_estimators, random_state=random_state, )

    # Making predictions
    base_predictions = base_clf.fit(X_train, y_train).predict(X_test)

    # Getting feature importance and sorting them in descending order
    important_features = pd.Series(data=base_clf.feature_importances_, index=X_train.columns)
    important_features.sort_values(ascending=False, inplace=True)

    # Measuring the f1_score of the predictions of the base classifier
    base_clf_fbeta_score = fbeta_score(y_test, base_predictions, 1, average="macro")

    # Storing each result
    result['base_clf_f1_score'] = base_clf_fbeta_score
    result['base_clf_n_estimators'] = base_clf_n_estimators

    # Showing each result
    print "F1 score on testing data: {:.4f}".format(base_clf_fbeta_score)


    # Dropping less important features
    if f_select_range:
        X_train_reduced = X_train[important_features[f_select_range[0]:f_select_range[1]].index.tolist()]
        X_test_reduced = X_test[important_features[f_select_range[0]:f_select_range[1]].index.tolist()]
    else:
        X_train_reduced = X_train
        X_test_reduced = X_test



    # Making AdaBoost classifier from the base classifier using the best parameters
    clf = AdaBoostClassifier(
        base_estimator=base_clf,
        random_state=random_state,
        n_estimators = boosting_clf_n_estimators,
        learning_rate = boosting_clf_learning_rate
    )

    # Make predictions
    predictions = clf.fit(X_train_reduced, y_train).predict(X_test_reduced)

    # Getting feature importance and sorting them in descending order
    important_features = pd.Series(data=clf.feature_importances_, index=X_train_reduced.columns)
    important_features.sort_values(ascending=False, inplace=True)

    # Measuring the F1 score of the predictions of the base classifier
    best_clf_fbeta_score = fbeta_score(y_test, predictions, 1, average="macro")

    # Storing each result
    result['best_clf_f1_score'] = best_clf_fbeta_score
    result['best_clf_n_estimators'] = boosting_clf_n_estimators
    result['best_clf_learning_rate'] = boosting_clf_learning_rate
    result['important_features'] = important_features
    result['time'] = (time.time() - start_time)

    # Showing each result
    print "\nFinal Model trained on reduced data\n------"
    print "F1 score on testing data: {:.4f}".format(best_clf_fbeta_score)
    print("--- %s seconds ---" % result['time'])
    return result

def train_and_measure_performance_3(random_state,features_final,target_var,f_select_range,n_estimators):

    # Getting start time of this process
    start_time = time.time()

    result = {}

    # Storing current random_state to the result
    result['random_state'] = random_state

    # Splitting the 'features' and 'sleep_quality' data into training and testing sets
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                        target_var,
                                                        test_size=test_size,
                                                        random_state=random_state)

    # Removing outliers
    outlier_detector = LocalOutlierFactor()  # Creating the object of LocalOutlierFactor
    detecting_outlier_result = outlier_detector.fit_predict(X_train)  # Getting the outliers and non-outliers

    # Extracting the indexes of non-outliers
    index_to_use = np.where(detecting_outlier_result == 1)[0].tolist()

    # Removing outliers from the training dataset
    X_train = X_train.iloc[index_to_use]
    y_train = y_train.iloc[index_to_use]

    # Making a base classifier (RandomForest), and finding the best parameters
    clf_1 = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state, )

    # Train the model and make predictions
    predictions = clf_1.fit(X_train, y_train).predict(X_test)

    # Getting feature importance and sorting them in descending order
    important_features = pd.Series(data=clf_1.feature_importances_, index=X_train.columns)
    important_features.sort_values(ascending=False, inplace=True)

    # Measuring the F1 score of the predictions of the classifier
    clf_1_fbeta_score = fbeta_score(y_test, predictions, beta=1,average="macro")

    # Storing each result
    result['clf_1_f1_score'] = clf_1_fbeta_score
    result['clf_1_n_estimators'] = n_estimators

    # Showing the F1 score
    print "F1 score on testing data: {:.4f}".format(clf_1_fbeta_score)

    # Dropping less important features
    if f_select_range:
        X_train_reduced = X_train[important_features[f_select_range[0]:f_select_range[1]].index.tolist()]
        X_test_reduced = X_test[important_features[f_select_range[0]:f_select_range[1]].index.tolist()]
    else:
        X_train_reduced = X_train
        X_test_reduced = X_test

    # Making a Random Forest Classifier again
    clf_2 = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state, )

    # Training with the reduced features
    predictions = clf_2.fit(X_train_reduced, y_train).predict(X_test_reduced)

    # Getting feature importance and sorting them in descending order
    important_features = pd.Series(data=clf_2.feature_importances_, index=X_train_reduced.columns)
    important_features.sort_values(ascending=False, inplace=True)
    clf_2_fbeta_score = fbeta_score(y_test, predictions, beta=1,average="macro")

    # Storing each result
    result['clf_2_f1_score'] = clf_2_fbeta_score
    result['clf_2_n_estimators'] = n_estimators
    result['important_features'] = important_features
    result['time'] = (time.time() - start_time)

    # Showing each result
    print "\nFinal Model trained on reduced data\n------"
    print "F1 score on testing data: {:.4f}".format(clf_2_fbeta_score)
    print("--- %s seconds ---" % result['time'])
    return result


def benchmark_train_and_measure_performance(features_final,target_var,random_state):
    result = {}


    # Splitting the data into training and testing sets
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                        target_var,
                                                        test_size=test_size,
                                                        random_state=random_state)

    # Making a classifier
    clf = GaussianNB()

    # Training the classifier and making the predictions for the test dataset
    predictions = (clf.fit(X_train, y_train)).predict(X_test)
    # print predictions

    #Testing and storing the result
    result['f1_score'] = fbeta_score(y_test, predictions, 1, average='macro')
    result['random_state'] = random_state

    # Showing the F1 score
    print "F1 score on testing data: {:.4f}".format(result['f1_score'])

    return result