"""
This visuals.vs contains processes which can be used for making visualization(plot)
"""

import sys
from collections import OrderedDict
class Visuals:

    def count_each_num_of_values_belong_to_each_range(self,df,num_of_classes,r_min,r_max,return_type='ordered_dict'):
        """
        It counts each number of values which belong to each range.
        First, it makes ranges like 0-30,30-60,60-90 according to given parameters.
        Then checks if each value in df is in one of the ranges. if so, add 1 to the range.
        In this case, if there 2 values between 0 and 30 such as 7 or 19, the count of 0-30 becomes 2.

        :param pandas.core.frame.DataFrame df: Pandas dataframe which you wish to count each number of values which belongs to each range.
        :param int num_of_classes: Number of classes (ranges) you wish to make. (ex: 3)
        :param int or float r_min: Minimum value which you wish to make ranges from.(ex: 0)
        :param int or float r_max: Maximum value which you wish to make ranges to .(ex: 90)
        :param string return_type: Format of the counts of each range you wish. 'ordered_dict' or 'tuple'
        :return collections.OrderedDict or tuples counts_of_each_range: Counts of each range,
        """
        total_range = r_max - r_min
        each_class_range = total_range / num_of_classes
        counts_of_each_range = OrderedDict()
        for i in range(0, num_of_classes):
            if i == 0:
                counts_of_each_range[str(r_min) + '-' + str((r_min + each_class_range))] = 0
            else:
                counts_of_each_range[str(r_min + (each_class_range * i) ) + '-' + str(r_min + (each_class_range * (i + 1)))] = 0
        for index, value in df.iteritems():
            for i in range(num_of_classes):
                if i == 0:
                    each_r_min = r_min
                    each_r_max = r_min + each_class_range
                else:
                    each_r_min = r_min + (each_class_range * i)
                    each_r_max = r_min + (each_class_range * (i + 1))
                key_name = str(each_r_min) + '-' + str(each_r_max)
                if each_r_min <= value < each_r_max:
                    counts_of_each_range[key_name] += 1
        if return_type == 'tuples':
            return tuple(counts_of_each_range.keys()),tuple(counts_of_each_range.values())
        return counts_of_each_range

    def count_each_num_of_values_belong_to_each_value(self,df,r_min,r_max,return_type='ordered_dict'):
        """
        Counts each number of values belong to each value (class).
        For example if there are 3 values of "2", the count of class of "2" becomes 3.

        :param pandas.core.frame.DataFrame df: Pandas dataframe which you wish to count each number of values belongs to each value (ex: 3)
        :param int or float r_min: Minimum value which you wish ro make ranges from.(ex: 0)
        :param int or float r_max: Maximum value which you wish ro make ranges to.(ex: 2)
        :param string return_type: Format of the counts of each range you wish. 'ordered_dict' or 'tuple'
        :return collections.OrderedDict counts_of_each_value :Counts of each value (class),
        """
        counts_of_each_value = OrderedDict()

        for i in range(r_min, r_max + 1):
            counts_of_each_value[i] = 0
        for index, value in df.iteritems():
            for i in range(r_min,r_max + 1):
                if i == value:
                    counts_of_each_value[i] += 1
        if return_type == 'tuples':
            return tuple(counts_of_each_value.keys()),tuple(counts_of_each_value.values())
        return counts_of_each_value


    def count_each_num_of_values_belongs_to_each_class(self,df,num_of_classes,r_min,r_max,return_type='ordered_dict'):
        """
        Counts each number of values belong to each class.
        According to the parameters you specify, This function will change the function to use.

        :param pandas.core.frame.DataFrame df: pandas dataframe which you wish to count each number of values belongs to each class.
        :param int or float r_min: Minimum value which you wish to make ranges from.
        :param int or float r_max: Maximum value which you wish to make ranges to.
        :param string return_type: Format of the counts of each range you wish. 'ordered_dict' or 'tuple'
        :return collections.OrderedDict or tuples: Counts of each class.
        """

        if num_of_classes == r_max + 1:
            return self.count_each_num_of_values_belong_to_each_value(df,r_min,r_max,return_type)
        else:
            return self.count_each_num_of_values_belong_to_each_range(df, num_of_classes, r_min, r_max,return_type)

    def display_min_and_max_values(self,df, column_name, label, separator):
        """
        Prints the max and min values of specified column of given dataframe

        :param pandas.core.frame.DataFrame df: Pandas dataframe which has a column you wish to print its max and min value.
        :param string column_name: Name of a column you wish to print its max and min value
        :param string label: Label to display in front of min and max values
        :param string separator: Separator you wish to use between min and max values.
        """
        print label + str(df[column_name].min()) + separator + str(df[column_name].max())

    def autolabel(self,ax,rects,fontsize = None,prec = 0):
        """
        Attach a text label above each bar displaying its height
        I implemented this method referencing following link.
        https://matplotlib.org/examples/api/barchart_demo.html

        :param matplotlib.axes._subplots.AxesSubplot ax:
        :param matplotlib.container.BarContainer rects: Bars which you wish add text to.
        :param int or float fontsize: Font size of the labels
        :param int prec: Number of digits after the decimal point of the labels
        """

        for rect in rects:
            height = rect.get_height()
            if prec >= 0:
                value = '{:.{prec}f}'.format(height, prec=prec)
            else:
                value = int(height)
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    value,
                    ha='center', va='bottom', fontsize=fontsize )