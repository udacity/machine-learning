import pandas as pd
import pre_process
import columns_config
import sys
import scipy.stats as ss
import matplotlib.pyplot as plt
all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")

#Dropping target values and storing to another variable.
features = all_data.drop('q30', axis = 1)
sleep_quality = all_data['q30']

#Making new features
all_data['Q43TOTAL'] = 0
all_data['Q36Q38Q40TOTAL'] = 0
# all_data['Q4Q3Q2Q1DIF'] = 0
all_data['Q3Q1DIF'] = 0
all_data['Q4Q2DIF'] = 0
all_data['Q4Q2DIFQ3Q1DIFTOTAL'] = 0

#Making a preprocess object
pre_process_obj = pre_process.PreProcess(all_data,columns_config.columns_config)

#Converting values, It is mainly imputation for missing data
pre_process_obj.convert_values()

#Converting types
# pre_process_obj.convert_types()

#Computing the values of the new features
sitting_hours_columns = ['Q43A','Q43B','Q43C','Q43D','Q43E','Q43F','Q43G1','Q43G2','Q43G3']
pre_process_obj.df['Q43TOTAL'] = pre_process_obj.df[sitting_hours_columns].sum(axis=1)
amount_of_exercise_columns= ['Q36','Q38','Q40']
pre_process_obj.df['Q36Q38Q40TOTAL'] = pre_process_obj.df[amount_of_exercise_columns].sum(axis=1)
pre_process_obj.df['Q3Q1DIF'] = pre_process_obj.df['Q3VALUE'] - pre_process_obj.df['Q1VALUE']
pre_process_obj.df['Q4Q2DIF'] = pre_process_obj.df['Q4VALUE'] - pre_process_obj.df['Q2VALUE']
pre_process_obj.df['Q4Q2DIFQ3Q1DIFTOTAL'] = pre_process_obj.df[['Q4Q2DIF','Q3Q1DIF']].sum(axis=1)

pre_process_obj.extract_data()
pre_process_obj.df.to_csv("first_refined_data_for_benchmark.csv")

