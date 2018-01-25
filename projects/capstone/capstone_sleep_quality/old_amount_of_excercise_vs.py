import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd
import visuals as vs
import matplotlib.pyplot as plt

all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
np.random.seed(19680801)
min = 0
max = 1600
num_of_classes = 8

# print Q36_classes
# print Q36_values
# sorted_Q36_distribution = sorted(Q36_distribution.items(), key=lambda x: x[0])
#
# print type(sorted_Q36_distribution)
# print sorted_Q36_distribution[0][0]
# print sorted(Q36_distribution.items(), key=lambda x: x[0])

# sys.exit()

# print vs.Visuals.classificate(all_data['Q38'], num_of_classes,min,max)
# print vs.Visuals.classificate(all_data['Q40'], num_of_classes,min,max)

N = num_of_classes
Q36_classes, Q36_values =  vs.Visuals.classificate(all_data['Q36'], num_of_classes,min,max,'tuples')
# print Q36_classes
# sys.exit()
# ind = np.arange(N)# the x locations for the groups
ind = np.arange(N)
# print ind
# sys.exit()
width = 0.35       # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(ind - (width / 2), Q36_values, width, color='r')# men's graph

# ax.legend(rects1[0], 'Men')


Q38_classes, Q38_values =  vs.Visuals.classificate(all_data['Q38'], num_of_classes,min,max,'tuples')
rects2 = ax.bar(ind + (width / 2), Q38_values, width, color='y')# women's graph

Q40_classes, Q40_values =  vs.Visuals.classificate(all_data['Q40'], num_of_classes,min,max,'tuples')
rects3 = ax.bar(ind + width + (width / 2), Q40_values, width, color='b')# women's graph

# add some text for labels, title and axes ticks
ax.set_ylabel('Number of samples')
ax.set_title('Minutes respondents spent for each type of exercise.')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(Q36_classes)
# ax.plot(kind='bar',legend = False,width = 2)
# ax.autoscale(tight=True)

# ax.legend((rects1[0], rects2[0],rects3[0]), ('Q36', 'Q38', 'Q40'))
ax.legend((rects1[0], rects2[0]), ('Q36', 'Q38'))

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.show()


# print all_data['Q36'].min()
# print all_data['Q36'].max()
# print all_data['Q38'].min()
# print all_data['Q38'].max()
# print all_data['Q40'].min()
# print all_data['Q40'].max()
sys.exit()






# The matplotlib.rcdefaults() command will restore the standard matplotlib default settings.
plt.rcdefaults()
# returns matplotlib.figure.Figure object and Axes object or array of Axes objects.
fig, ax = plt.subplots(2)
# print ax
# print ax[0]
# print ax[1]
# sys.exit()

# classes = np.array([
#     '1',
#     '2',
#     '3',
#     '4',
#     '5',
#     '6',
#     '7',
#     '8',
#     '9',
#     '10',
#     '11',
#     '12',
#     '13',
#     '14',
#     '15',
#     '16',
#     '17',
#     '18',
#     '19',
#     '20',
#     '21',
#     '22',
#     '23'
# ])
y_labels = np.array([
    '12:00 AM (Midnight)',
    '12:01 AM to 12:59 AM',
    '1:00 AM to 1:59 AM',
    '2:00 AM to 5:00 AM',
    '5:01 AM to 8:59 AM',
    '9:00 AM to 11:59 AM',
    '12:00 PM (Noon) to 6:59 PM',
    '7:00 PM to 7:59 PM',
    '8:00 PM to 8:59 PM',
    '9:00 PM to 9:14 PM',
    '9:15 PM to 9:29 PM',
    '9:30 PM to 9:44 PM',
    '9:45 PM to 9:59 PM',
    '10:00 PM to 10:14 PM',
    '10:15 PM to 10:29 PM',
    '10:30 PM to 10:44 PM',
    '10:45 PM to 10:59 PM',
    '11:00 PM to 11:14 PM',
    '11:15 PM to 11:29 PM',
    '11:30 PM to 11:44 PM',
    '11:45 PM to 11:59 PM',
    'Refused',
    'Don\'t know',
])
dummies_q1= pd.get_dummies(all_data['q1'])
dummies_q3= pd.get_dummies(all_data['q3'])
dummies_q3[7] = 0
# dummies_q3.reindex(sorted(dummies_q3.columns))
# print dummies_q3
dummies_q3 = dummies_q3.sort_index(axis=1)
# print dummies_q3.keys()
print len(dummies_q1.keys())
# print len(dummies_q3.keys())
# print type(dummies_q3)
# print len(y_labels)
# sys.exit()
# print dummies
# sys.exit()

def get_sum_of_each_category(dummies):
        sum_of_each_category_dict = {}
        for index, row in dummies.iterrows():
                for index_2, value in row.iteritems():
                        if index_2 not in sum_of_each_category_dict:
                                sum_of_each_category_dict[index_2] = 0
                        if value == 1:
                                sum_of_each_category_dict[index_2] += 1
        # print sum_of_each_category_dict
        # sys.exit()
        sum_of_each_category = np.array(list(sum_of_each_category_dict.values()))
        return sum_of_each_category

# sum_of_each_category_q1 = get_sum_of_each_category(dummies_q1)
sum_of_each_category_q3 = get_sum_of_each_category(dummies_q3)
# print sum_of_each_category_q3
# print len(sum_of_each_category_q3)
# sys.exit()
# sum_of_each_category_dict = {}
# for index, row in dummies.iterrows():
#     for index_2, value  in row.iteritems():
#         if value == 1:
#             if index_2 not in sum_of_each_category_dict:
#                 sum_of_each_category_dict[index_2] = 0
#             sum_of_each_category_dict[index_2] += 1
# sum_of_each_category= np.array(list(sum_of_each_category_dict.values()))
#
# print sum_of_each_category
# sys.exit()


# people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')# define people
# seems to return series which contains five values from zero
y_pos = np.arange(len(y_labels))

# print y_pos
# sys.exit()
# performance = 3 + 10 * np.random.rand(len(people))
# error = np.random.rand(len(people))# just return 5 random values
# print performance
# sys.exit()
#Make a horizontal bar plot
# xerr specifies error bars, and ecolor specifies the color of the error bars/
ax[0].barh(y_pos, sum_of_each_category_q1, align='center',
        color='blue')
ax[0].set_yticks(y_pos) # it specifies y values
ax[0].set_yticklabels(y_labels) #specify people y tick labels
ax[0].invert_yaxis()  # labels read top-to-bottom
ax[0].set_xlabel('Number of each answers')# lbel for x axis
ax[0].set_title('what time do you get into bed in a week day')# specifies title

ax[1].barh(y_pos, sum_of_each_category_q3, align='center',
        color='blue')
ax[1].set_yticks(y_pos) # it specifies y values
ax[1].set_yticklabels(y_labels) #specify people y tick labels
ax[1].invert_yaxis()  # labels read top-to-bottom
ax[1].set_xlabel('Number of each answers')# lbel for x axis
ax[1].set_title('what time do you get into bed in a week day')# specifies title

plt.show()