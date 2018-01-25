import pandas as pd
import numpy as np
# import pre_process
# import columns_config
import sys
import matplotlib.pyplot as plt

all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")

# DO NOT ERASE. Visualization of qs1
# all_data.qs1.plot(kind='kde',rot=10)
# print all_data['qs1'].min()
# print all_data['qs1'].max()
# all_data['qs1'].hist(bins=8,range=(20,60))

# all_data['q1'].hist(bins=21,range=(1,21))
left = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,98,99])
# labels = np.array([
#     '12:00 AM (Midnight)',
#     '12:01 AM to 12:59 AM',
#     '1:00 AM to 1:59 AM',
#     '2:00 AM to 5:00 AM',
#     '5:01 AM to 8:59 AM',
#     '9:00 AM to 11:59 AM',
#     '12:00 PM (Noon) to 6:59 PM',
#     '7:00 PM to 7:59 PM',
#     '8:00 PM to 8:59 PM',
#     '9:00 PM to 9:14 PM',
#     '9:15 PM to 9:29 PM',
#     '9:30 PM to 9:44 PM',
#     '9:45 PM to 9:59 PM',
#     '10:00 PM to 10:14 PM',
#     '10:15 PM to 10:29 PM',
#     '10:30 PM to 10:44 PM',
#     '10:45 PM to 10:59 PM',
#     '11:00 PM to 11:14 PM',
#     '11:15 PM to 11:29 PM',
#     '11:30 PM to 11:44 PM',
#     '11:45 PM to 11:59 PM',
#     'Refused',
#     'Don\'t know',
# ])
# print labels
# sys.exit()
labels = np.array([
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    '16',
    '17',
    '18',
    '19',
    '20',
    '21',
    '22',
    '23'
])
dummies = pd.get_dummies(all_data['q1'])
sum_of_each_category_dict = {}
for index, row in dummies.iterrows():
    for index_2, value  in row.iteritems():
        if value == 1:
            if index_2 not in sum_of_each_category_dict:
                sum_of_each_category_dict[index_2] = 0
            sum_of_each_category_dict[index_2] += 1
sum_of_each_category= np.array(list(sum_of_each_category_dict.values()))
# labels = np.array(list(sum_of_each_category_dict.keys()))
sum_of_each_category = sum_of_each_category[:len(sum_of_each_category)-2]
labels = labels[:len(labels)-2]
left = left[:len(left)-2]
# print len(sum_of_each_category)
# print len(labels)
# sys.exit()
# labels_2 = np.array(list(sum_of_each_category_dict.keys()))
# # print sum_of_each_category
# # print labels
# print labels_2
# print len(sum_of_each_category)
# # print len(labels)
# print len(labels_2)
# sys.exit()
# print all_data['q1'].values
# print type(all_data['q1'].values)
# sys.exit()
# df = pd.Series(all_data['q1'].values)
# cumsum = df.groupby(labels).sum()
plt.bar(left,sum_of_each_category,tick_label=labels,bottom=100)


plt.show()
sys.exit()




# bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# all_data['binned_age'] = pd.cut(all_data['qs1'],bins)
# print all_data['binned_age']
# sys.exit()
# # all_data['qs1'].hist(bins=60)
# all_data['binned_age'].plot(kind='bar')
# plt.show()
# print all_data
sys.exit()