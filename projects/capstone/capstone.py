import numpy as np
import pandas as pd
from time import time
from sklearn.model_selection import KFold
import sys
from sklearn.metrics import r2_score


#import files
all_data = pd.read_csv("hw-spr2007-anon-demographics-1.csv")
refined_data = all_data[:-(len(all_data) - 76)]

#pre_process the data
columns_to_rename={'Condition': 'condition' , 'Pre-Test\r\nForm': 'pre_test', 'Post-Test': 'post_test', 'Retention\r\nTest': 'retention_test'}
columns_to_extract = ['condition','pre_test','post_test','retention_test' ]

def rename_columns(data, columns_to_rename):
    data = data.rename(
        columns=columns_to_rename
    )
    return data
renamed_data = rename_columns(refined_data, columns_to_rename)
extracted_data = renamed_data[columns_to_extract]
extracted_data.is_copy = False # this will prevent warning

score_gragdes_table = {'A': 3, 'B': 2, 'C': 1}
columns_to_convert = ['pre_test','post_test','retention_test']

def convert_gragdes(data,columns_to_convert,score_gragdes_table ):
    for org_grade, new_grade in score_gragdes_table.iteritems():
        for column in columns_to_convert:
            data.loc[data[column] == org_grade, column] = new_grade
    return data
grades_converted_data = convert_gragdes(extracted_data,columns_to_convert,score_gragdes_table)

#calculate improvments
grades_converted_data["condition"] = grades_converted_data["condition"].astype(int)
# improvements = []
def calculate_improvments(data):
    improvements = []
    for index, row in data.iterrows():
        improvements.append(row['post_test'] - row['pre_test'])
    return improvements
improvements = calculate_improvments(grades_converted_data)


# one hot encode conditions
one_hot_encoded_conditions = pd.get_dummies(grades_converted_data['condition'],prefix='condition')

#set x and y
X = one_hot_encoded_conditions.values
y = np.array( improvements )

def get_k_folded_data(X, y, random_state):
    kf = KFold(n_splits=4, shuffle=True, random_state=random_state)
    rearranged = {}
    k = 0

    X_tests = {}
    y_tests = {}
    for train_index, test_index in kf.split(X):
        # print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        X_tests[k] = X_test
        y_tests[k] = y_test

        if not k in rearranged:
            rearranged[k] = {}
        for (x_index_1, x_index_2), x_value in np.ndenumerate(X_train):
            if x_value == 1:
                condition = x_index_2 + 1
                if not condition in rearranged[k]:
                    rearranged[k][condition] = []
                rearranged[k][condition].append(y_train[x_index_1])
                continue
        k += 1

    X_tests = np.concatenate((X_tests[0], X_tests[1], X_tests[2], X_tests[3]), axis=0)
    y_tests = np.concatenate((y_tests[0], y_tests[1], y_tests[2], y_tests[3]), axis=0)
    return rearranged, X_tests, y_tests
random_state = 0
rearranged_data, X_tests, y_tests = get_k_folded_data(X, y,random_state)

def get_final_averages(data):
    averages = {}
    sums = {}
    for k, each_set in data.iteritems():
        if not k in averages:
            averages[k] = {}
        for condition, value in each_set.iteritems():
            averages[k][condition] = np.mean(value)
            if not condition in  sums:
                sums[condition] = 0
            sums[condition] += averages[k][condition]

    final_averages = {}

    for key, sum in sums.iteritems() :
        final_averages[key] = sum / len(data)
    return final_averages

final_averages = get_final_averages(rearranged_data)


def get_predictions(X_tests,final_averages):
    predictions = []
    i = 0
    for conditions in X_tests:
        for key, value in np.ndenumerate(conditions):
            if value == 1:
                predictions.append(final_averages[key[0] + 1])
                continue
        i += 1
    return predictions

predictions = get_predictions(X_tests, final_averages)

print predictions


print r2_score(y_tests, predictions)

#test modification