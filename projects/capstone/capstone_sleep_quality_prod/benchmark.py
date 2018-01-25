import pandas as pd
import pre_process
import columns_config

#Getting preprocessed Data
# refined_data = pd.read_csv("first_refined_data.csv")
refined_data = pd.read_csv("first_refined_data_for_benchmark.csv")
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
    # Importing necessary libraries
    from sklearn.cross_validation import train_test_split
    from sklearn.metrics import fbeta_score, accuracy_score
    from sklearn.naive_bayes import GaussianNB

    # Splitting the data into training and testing sets
    random_state = 0
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(features_final,
                                                        target_var,
                                                        test_size=test_size,
                                                        random_state=random_state)

    # Making a classifier
    clf = GaussianNB()

    # Training the classifier and making the predictions for the test dataset
    predictions = (clf.fit(X_train, y_train)).predict(X_test)

    #Testing and showing the result
    print "Accuracy on testing data: {:.4f}".format(accuracy_score(y_test, predictions))

train_and_measure_the_performance(features_final,sleep_quality['q30'])









