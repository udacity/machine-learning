import numpy as np
import pandas as pd
import sys
import math


def convert_values_and_extract_columns(data, columns_info):
    # print columns_info
    # sys.exit()
    columns_to_extract = []
    mean = 0

    for column_name, empty_values_setting in columns_info.items():

        # print column_name
        if any(empty_values_setting): #convert empty values

            # To convert to mean, we have to replace numeric values with NaN,
            # and calculate mean
            for convert_from, convert_to in empty_values_setting.items():
                for key, value in data[column_name].iteritems():
                    if convert_to != "_mean" and ((convert_from == "_NaN" and pd.isnull(value)) or convert_from == value):
                        data.loc[key, column_name] = convert_to

            # after converted other values, calculate mean
            if '_mean' in empty_values_setting.values():
                tmp_data = data.copy(deep = True)
                for convert_from, convert_to in empty_values_setting.iteritems():
                    if convert_to == '_mean':
                        tmp_data[column_name] = tmp_data[column_name].replace(convert_from, np.NaN)
                mean = average(tmp_data[column_name])

            # insert mean
            for convert_from, convert_to in empty_values_setting.items():
                for key, value in data[column_name].iteritems():
                    if convert_to == "_mean" and convert_from == value:
                        data.loc[key, column_name] = mean
        columns_to_extract.append(column_name)
    return data[columns_to_extract]


def average(data):
    sum = i = 0
    for key, value in data.iteritems():
        if isinstance(value, (int, np.integer, float)) and not math.isnan(value) :
            sum += value
            i += 1
    return float(sum) / float(i)

