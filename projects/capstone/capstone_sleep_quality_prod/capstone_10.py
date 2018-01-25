#Importing necessary modules, classes and methods
import pandas as pd
import pre_process
import columns_config
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.cross_validation import train_test_split
from sklearn.metrics import fbeta_score, accuracy_score
from sklearn.ensemble import RandomForestClassifier
import sys

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

#Getting final features
features_final = pre_process_obj.df

def train_and_measure_the_performance(features_final,target_var):
    # Splitting the data into training and testing sets
    random_state = 1
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                        target_var,
                                                        test_size=test_size,
                                                        random_state=random_state)

    # Making a base classifier, and finding the best classifier
    base_clf = RandomForestClassifier(random_state=random_state)
    parameters = {'n_estimators': [90, 100, 110, 120, 130, 140, 150, 160, 170,180, 190 ,200]}
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


feature_importance = train_and_measure_the_performance(features_final,sleep_quality['q30'])
print feature_importance
print refined_data.corr()['q30'].sort_values(ascending=False)






