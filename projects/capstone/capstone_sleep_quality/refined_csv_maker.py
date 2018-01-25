import pandas as pd
import pre_process
import columns_config
import sys
import scipy.stats as ss
import matplotlib.pyplot as plt
all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
# pd.set_option("display.max_colwidth", 1000)
# pd.set_option("display.max_rows", 1000)
# print all_data.dtypes
# sys.exit()
# print len(all_data.keys())
# print len(columns_config.columns_config.keys())
# sys.exit()
#Dropping target values and storing to another variable.
features = all_data.drop('q30', axis = 1)
sleep_quality = all_data['q30']


all_data['Q43TOTAL'] = 0
all_data['Q36Q38Q40TOTAL'] = 0
# all_data['Q4Q3Q2Q1DIF'] = 0
all_data['Q3Q1DIF'] = 0
all_data['Q4Q2DIF'] = 0
all_data['Q4Q2DIFQ3Q1DIFTOTAL'] = 0
#Making a preprocess object
pre_process_obj = pre_process.PreProcess(all_data,columns_config.columns_config)

#Making and Adding new features


pre_process_obj.convert_values()
pre_process_obj.convert_types()

#Making and Adding new features
sitting_hours_columns = ['Q43A','Q43B','Q43C','Q43D','Q43E','Q43F','Q43G1','Q43G2','Q43G3']
pre_process_obj.df['Q43TOTAL'] = pre_process_obj.df[sitting_hours_columns].sum(axis=1)
amount_of_exercise_columns= ['Q36','Q38','Q40']
pre_process_obj.df['Q36Q38Q40TOTAL'] = pre_process_obj.df[amount_of_exercise_columns].sum(axis=1)
pre_process_obj.df['Q3Q1DIF'] = pre_process_obj.df['Q3VALUE'] - pre_process_obj.df['Q1VALUE']
pre_process_obj.df['Q4Q2DIF'] = pre_process_obj.df['Q4VALUE'] - pre_process_obj.df['Q2VALUE']
pre_process_obj.df['Q4Q2DIFQ3Q1DIFTOTAL'] = pre_process_obj.df[['Q4Q2DIF','Q3Q1DIF']].sum(axis=1)


pre_process_obj.raise_values_to_positive()
# res = pre_process_obj.get_skews().abs()
# res.sort_values(ascending=False, inplace=True)
# print res[]
# sys.exit()
pre_process_obj.set_log_trans_based_on_skewness(1.50)
pre_process_obj.apply_log_trans_according_to_columns_config()
# # print pre_process_obj.get_column_names_to_apply_log_trans()
# columns = pre_process_obj.get_column_names_to_apply_log_trans()
# print columns
# print pre_process_obj.df[columns]
# print pre_process_obj.get_skews()
# plt.hist(pre_process_obj.df['STOPBAG2'],50)
# plt.show()
# sys.exit()
# sys.exit()
# print len(pre_process_obj.df.keys())
# sys.exit()

# pre_process_obj.df['Q4Q3Q2Q1DIF'] = pre_process_obj.df['Q4Q3DIF'] - pre_process_obj.df['Q2Q1DIF']

# pre_process_obj.extract_data()



#Converting some values to absolute values
# pre_process_obj.apply_abs()
# print pre_process_obj.df['Q4Q3DIF']
# # print pre_process_obj.df['Q2Q1DIF']
# # print pre_process_obj.df['Q4Q3Q2Q1DIF']
# sys.exit()

#Applying logistic transformation to certain columns
# pre_process_obj.apply_log_trans

# plt.hist(pre_process_obj.df['EPWORTH'],50)
# plt.show()
# sys.exit()

#Recalculating certain columns such as
# pre_process_obj.recalculation()

# print pre_process_obj.df
#
# result = pre_process_obj.are_valid_data()
# print result
# pd.set_option("display.max_colwidth", 1000)
# pd.set_option("display.max_rows", 1000)
# print pre_process_obj.df[['Q43TOTAL']]
# sys.exit()
pre_process_obj.extract_data()
pre_process_obj.df.to_csv("first_refined_data.csv")

