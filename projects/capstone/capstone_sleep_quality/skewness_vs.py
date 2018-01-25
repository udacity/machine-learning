import pandas as pd
import pre_process
import columns_config
import sys
import scipy.stats as ss
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")



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
# print pre_process_obj.df['Q4Q3Q2Q1DIF'].abs()
# print pre_process_obj.df['Q4Q3DIF']
# print pre_process_obj.df['Q2Q1DIF']
# print pre_process_obj.df['Q4Q3Q2Q1DIF']
# sys.exit()
#Converting values and extracting the data
# pre_process_obj.convert_values_and_extract_data()
#
# print pre_process_obj.df['Q4Q3DIF']
# # sys.exit()

pre_process_obj.convert_values()
pre_process_obj.convert_types()

sitting_hours_columns = ['Q43A','Q43B','Q43C','Q43D','Q43E','Q43F','Q43G1','Q43G2','Q43G3']
pre_process_obj.df['Q43TOTAL'] = pre_process_obj.df[sitting_hours_columns].sum(axis=1)
amount_of_exercise_columns= ['Q36','Q38','Q40']
pre_process_obj.df['Q36Q38Q40TOTAL'] = pre_process_obj.df[amount_of_exercise_columns].sum(axis=1)
pre_process_obj.df['Q3Q1DIF'] = pre_process_obj.df['Q3VALUE'] - pre_process_obj.df['Q1VALUE']
pre_process_obj.df['Q4Q2DIF'] = pre_process_obj.df['Q4VALUE'] - pre_process_obj.df['Q2VALUE']
pre_process_obj.df['Q4Q2DIFQ3Q1DIFTOTAL'] = pre_process_obj.df[['Q4Q2DIF','Q3Q1DIF']].sum(axis=1)


# print pre_process_obj.get_column_names_contain_continuous_values()
# sys.exit()
# print len(pre_process_obj.df.keys())
# sys.exit()
# print ss.skew(features['Q36'])
column_names_contain_continuous_values = pre_process_obj.get_column_names_contain_continuous_values()
skews = []
for column_name in column_names_contain_continuous_values:
    skews.append(ss.skew(pre_process_obj.df[column_name]))
skews_series = pd.Series(data=skews, index=column_names_contain_continuous_values)
skews_series.sort_values(ascending=False, inplace=True)
# print pre_process_obj.df['Q6Q5DIF']
# print pre_process_obj.df['Q6Q5DIF'].isnull().values.any()
print skews_series
sys.exit()

print pre_process_obj.df['q29a'].max()
plt.hist(pre_process_obj.df['q29a'],50)
plt.show()
sys.exit()

# pre_process_obj.df['Q4Q3Q2Q1DIF'] = pre_process_obj.df['Q4Q3DIF'] - pre_process_obj.df['Q2Q1DIF']

pre_process_obj.extract_data()

print pre_process_obj.df.keys()
sys.exit()


#Converting some values to absolute values
pre_process_obj.apply_abs()
# print pre_process_obj.df['Q4Q3DIF']
# # print pre_process_obj.df['Q2Q1DIF']
# # print pre_process_obj.df['Q4Q3Q2Q1DIF']
# sys.exit()

#Applying logistic transformation to certain columns
pre_process_obj.apply_log_trans()



#Recalculating certain columns such as
pre_process_obj.recalculation()

# print pre_process_obj.df
#
# result = pre_process_obj.are_valid_data()
# print result
# pd.set_option("display.max_colwidth", 1000)
# pd.set_option("display.max_rows", 1000)
# print pre_process_obj.df[['Q43TOTAL']]
# sys.exit()
pre_process_obj.df.to_csv("first_refined_data.csv")

