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

print 'ok'
test = {
    'one':{98:'_mean',99:'_mean','_NaN':'mean',94:'something'},
    'two': {98:'_mean'}
}
print test
sys.exit()

all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
# print list(all_data)
# sys.exit()
# print type(all_data)
# sys.exit()
# all_data.drop(['caseid', 'source','market','smptype','city','state','zip'
#                   ,'fips','dma','tz','rep','census','age','qs1a','','',''], axis=1)
# print all_data
# sys.exit()
#

# print type(all_data["NORTHEAST"][0])
# sys.exit()
# refined_data =  all_data[["qs1","qs2","qs3","NORTHEAST","MIDWEST","SOUTH","WEST","Q1VALUE","Q2VALUE",
#                       "Q2Q1DIF","Q3VALUE","Q4VALUE","Q4Q3DIF","Q4Q3Q2Q1DIFHRS","Q5","Q6","Q6Q5DIF"
#     ,"q7","q8","q9","q10","q11","q12","q13a","q13b","q13c","q13d","q13e","q13f","q13g","EPWORTH",
#                       "q14","q15","q16a","q16c","q16d","q16e","q16f","q17","q18","q19a","q19b",
#                       "q19c","q19d","q20","q21","q22","q23","q24","q25","q26","q27","q28","q29a","q29b","q29c",
#                       "Q29TOTAL","q30","q31","q32","q33","q34","q35","Q36","q3701","q3702","q3703","Q38"
# ,"q3901","q3902","q3903","Q40","q4101","q4102","q4103","Q42","Q43A","Q43B","Q43C","Q43D","Q43E","Q43F","Q43G1"
#     ,"Q43G2","Q43G3","q4401","q4402","q4403","q45","q46","q47","q48","q49","q50","SHEEWORK","SHEEFAMILY","SHEEMOOD"
#     ,"SHEESEX","SHEETOTAL","NSFDISABLE","WEIGHT","HEIGHT","BMI","STOPBAG1","STOPBAG2","IPAQ36","IPAQ38","IPAQ40","IPAQTOTAL"]]
# all_data =  all_data[["Q1VALUE"]]
# print 9998 == 9998.00
# print all_data['Q1VALUE'][97]
# print all_data
# sys.exit()
columns_info = {
    'qs1':{
        '_NaN':'_mean'
    },
    'qs2':{
        '_NaN':94
    },
    'qs3':{
        '_NaN':94
    },
    'NORTHEAST':{
        '_NaN':0
    },
    'MIDWEST':{
        '_NaN':0
    },
    'SOUTH':{
        '_NaN':0
    },
    'WEST':{
        '_NaN':0
    },
    'Q1VALUE':{
        9998:'_mean',
        9999:'_mean'
    },
    'Q2VALUE':{
        9998:'_mean',
        9999:'_mean'
    },
    'Q2Q1DIF':{
    #     recalculate
    },
    'Q3VALUE':{
        9998:'_mean',
        9999:'_mean'
    },
    'Q4VALUE':{
        9998:'_mean',
        9999:'_mean'
    },
    'Q4Q3DIF':{
    #     recalculate
    },
    'Q4Q3Q2Q1DIFHRS':{
    #     recalculate
    },
    'Q5':{
        '_NaN':'_mean'
    },
    'Q6':{
        '_NaN':'_mean'
    },
    'Q6Q5DIF':{
        #     recalculate
    },
    'q7':{
        '_NaN':94
    },
    'q8':{
        '_NaN':94
    },
    'q9':{
        '_NaN':94
    },
    'q10':{
        '_NaN':94
    },
    'q11':{
        '_NaN':94
    },
    'q12':{
        '_NaN':94
    },
    'q13a':{
        '_NaN':94
    },
    'q13b':{
        '_NaN':94
    },
    'q13c':{
        '_NaN':94
    },
    'q13d':{
        '_NaN':94
    },
    'q13e':{
        '_NaN':94
    },
    'q13f':{
        '_NaN':94
    },
    'q13g':{
        '_NaN':94
    },
    'EPWORTH':{
        '_NaN':'_mean'
    },
    'q14':{
        '_NaN':94
    },
    'q15':{
        '_NaN':94
    },
    'q16a':{
        '_NaN':94
    },
    'q16c':{
        '_NaN':94
    },
    'q16d':{
        '_NaN':94
    },
    'q16e':{
        '_NaN':94
    },
    'q16f':{
        '_NaN':94
    },
    'q17':{
        '_NaN':94
    },
    'q18':{
        '_NaN':94
    },
    'q19a':{
        '_NaN':94
    },
    'q19b':{
        '_NaN':94
    },
    'q19c':{
        '_NaN':94
    },
    'q19d':{
        '_NaN':94
    },
    'q20':{
        '_NaN':94
    },
    'q21':{
        '_NaN':94
    },
    'q22':{
        '_NaN':94
    },
    'q23':{
        '_NaN':94
    },
    'q24':{
        '_NaN':94
    },
    'q25':{
        '_NaN':94
    },
    'q26':{
        '_NaN':94
    },
    'q27':{
        '_NaN':94
    },
    'q28':{
        '_NaN':94
    },
    'q29a':{
        '_NaN':94
    },
    'q29b':{
        '_NaN':94
    },
    'q29c':{
        '_NaN':94
    },
    'Q29TOTAL':{
        98:'_mean',
        99:'_mean'
    },
    'q30':{
        '_NaN':94
    },
    'q31':{
        '_NaN':94
    },
    'q32':{
        '_NaN':94
    },
    'q33':{
        '_NaN':94
    },
    'q34':{
        '_NaN':94
    },
    'q35':{
        '_NaN':'mean',
        996:'_mean',
        998:'_mean',
        999:'_mean'
    },
    'Q36':{
        98:'_mean',
        99:'_mean',
        '_NaN':'mean',
    },
    'q3701':{
        '_NaN':94
    },
    'q3702':{
        '_NaN':94
    },
    'q3703':{
        '_NaN':94
    },

    'Q38':{
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },

    'q3901': {
        '_NaN': 94
    },
    'q3902': {
        '_NaN': 94
    },
    'q3903': {
        '_NaN': 94
    },
    'q4101':{
        '_NaN':94
    },
    'q4102':{
        '_NaN':94
    },
    'q4103':{
        '_NaN':94
    },
    'Q42':{
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },
    'Q43A':{
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },
    'Q43B':{
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },
    'Q43C':{
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },
    'Q43D':{
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },

    'Q43E': {
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },

    'Q43F': {
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },
    'Q43G1': {
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },
    'Q43G2': {
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },
    'Q43G3': {
        98: '_mean',
        99: '_mean',
        '_NaN': 'mean'
    },
    'q4401': {
        '_NaN': 94
    },
    'q4402': {
        '_NaN': 94
    },
    'q4403': {
        '_NaN': 94
    },
    'q45': {
        '_NaN': 94
    },
    'q46': {
        '_NaN': 94
    },
    'q47': {
        '_NaN': 94
    },
    'q48': {
        '_NaN': 94
    },
    'q49': {
        '_NaN': 94
    },
    'q50': {
        '_NaN': 94
    },
    'q51': {
        '_NaN': 94
    },
    'q53': {
        '_NaN': 94
    },
    'q54': {
        '_NaN': 94
    },
    'q55': {
        '_NaN': 94
    },
    'q56': {
        '_NaN': 94
    },
    'q5701': {
        '_NaN': 94
    },
    'q5702': {
        '_NaN': 94
    },
    'q5703': {
        '_NaN': 94
    },
    'q5704': {
        '_NaN': 94
    },
    'SHEEWORK': {
        '_NaN': '_mean'
    },
    'SHEEFAMILY': {
        '_NaN': '_mean'
    },
    'SHEESOCIAL': {
        '_NaN': '_mean'
    },
    'SHEEMOOD': {
        '_NaN': '_mean'
    },
    'SHEESEX': {
        '_NaN': '_mean'
    },
    'SHEETOTAL': {
        '_NaN': '_mean'
    },
    'NSFDISABLE': {
        '_NaN': '_mean'
    },
    'WEIGHT': {
        '_NaN': '_mean'
    },
    'HEIGHT': {
        '_NaN': '_mean'
    },
    'BMI': {
        '_NaN': '_mean'
    },
    'STOPBAG1': {
        '_NaN': 0
    },
    'STOPBAG2': {
        '_NaN': '_mean'
    },
    'IPAQ36': {
        '_NaN': '_mean',
        98: '_mean',
        99: '_mean'
    },
    'IPAQ38': {
        '_NaN': '_mean',
        98: '_mean',
        99: '_mean'
    },
    'IPAQ40': {
        '_NaN': '_mean',
        98: '_mean',
        99: '_mean'
    },
    'IPAQTOTAL': {
        '_NaN': 94,
        98: '_mean',
        99: '_mean'
    }




}



def convert_values_and_extract_columns(data, columns_info):

    columns_to_extract = []
    for column_name, empty_values_setting in columns_info.items():
        print column_name
        if any(empty_values_setting): #convert empty values
            # To convert to mean, we have to replace numeric values with NaN,
            # and calculate mean
            if '_mean' in empty_values_setting.values():
                convert_to_mean = {}
                for convert_from, convert_to in empty_values_setting.iteritems():
                    if convert_to == '_mean' and convert_from != '_NaN':
                        data[column_name] = data[column_name].replace(convert_from, np.NaN)
                mean = data[column_name].mean()
            for convert_from, convert_to in empty_values_setting.items():
                for key, value in data[column_name].iteritems():
                    if (convert_from == "_NaN" and pd.isnull(value)) or convert_from == value:
                        if convert_to == "_mean":
                            convert_to = mean
                        data.loc[key, column_name] = convert_to
        columns_to_extract.append(column_name)
    return data, columns_to_extract



refined_data, columns_to_extract=  convert_values_and_extract_columns(all_data,columns_info)

# print type(refined_data)
# sys.exit()
def extract_values():

    return
# print len(refined_data.columns)
print refined_data['Q1VALUE'][97]
sys.exit()

# features =  all_data[["q34","q35"]]
# qualities_of_sleep = all_data["q30"]
# TODO: Train the supervised model on the training set using .fit(X_train, y_train)
random_state = 0


clf = AdaBoostClassifier(random_state = random_state)
X_train, X_test, y_train, y_test = train_test_split(features,
                                                    qualities_of_sleep,
                                                    test_size = 0.2,
                                                    random_state = random_state)

clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
# print predictions
print accuracy_score(y_test,predictions)
# TODO: Extract the feature importances using .feature_importances_
# importances = model.feature_importances_

# Plot
# vs.feature_plot(importances, X_train, y_train)
