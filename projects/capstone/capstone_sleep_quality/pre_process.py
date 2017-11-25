import numpy as np
import pandas as pd
import sys
import math
import str


def convert_values_and_extract_data(data, columns_info):
    columns_to_extract = []
    mean = 0
    for column_name, column_info_2 in columns_info.items():
        if 'conversion' in column_info_2 and any(column_info_2['conversion']): #convert empty values

            # To convert to mean, we have to replace the numeric values with NaN,
            # then calculate mean
            for convert_from, convert_to in column_info_2['conversion'].items():
                for key, value in data[column_name].iteritems():
                    if convert_to != "_mean" and ((convert_from == "_NaN" and pd.isnull(value)) or convert_from == value):
                        # if convert_to == 94:
                        #     print convert_to
                        #     print type(convert_to)
                        data.loc[key, column_name] = convert_to

            # after converted other values, calculate mean
            if '_mean' in column_info_2['conversion'].values():
                tmp_data = data.copy(deep = True)
                for convert_from, convert_to in column_info_2['conversion'].iteritems():
                    if convert_to == '_mean':
                        tmp_data[column_name] = tmp_data[column_name].replace(convert_from, np.NaN)
                mean = average(tmp_data[column_name])

            # insert mean
            for convert_from, convert_to in column_info_2['conversion'].items():
                for key, value in data[column_name].iteritems():
                    if convert_to == "_mean" and (convert_from == value or convert_from == '_NaN' and pd.isnull(value)):
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

def recalculation(data, columns_info):
    for column_name, column_info in columns_info.items():
        if 'recalculation' in column_info and any(column_info['recalculation']):
            if 'subtraction' in column_info['recalculation'] \
                    and any(column_info['recalculation']['subtraction']):
                i = 0
                for column_name_2 in column_info['recalculation']['subtraction']:
                    if i == 0:
                        data[column_name] = data[column_name_2]
                    else:
                        data[column_name] = data[column_name] - data[column_name_2]
                    i += 1
    return data

def get_one_hot_encode_list(columns_info):
    one_hot_encode_list = []
    for column_name, column_info in columns_info.items():
        if 'one_hot_encoding' in column_info and column_info['one_hot_encoding'] == True:
            one_hot_encode_list.append(column_name)
    return one_hot_encode_list


def apply_one_hot_encode(data,columns_info):
    one_hot_encode_list = get_one_hot_encode_list(columns_info)
    one_hot_encoded_data = pd.get_dummies(data=data, columns=one_hot_encode_list)
    return one_hot_encoded_data

""
def are_valid_data(data,columns_info):
    result = {}
    i = 0
    for column_name, column_info in columns_info.items():
        available_values = []

        # if 'available_values' are set in column_info, the value in the data must be in the available_values
        if 'available_values' in column_info \
                and type(column_info['available_values']) is list \
                and any(column_info['available_values']):
            available_values.extend(column_info['available_values'])

            # store the value of convert_to to available_values
            if 'conversion' in column_info and any(column_info['conversion']):
                for convert_from, convert_to in column_info['conversion'].items():
                    if convert_to == '_NaN': # if '_NaN', set NaN to convert_to
                        convert_to = float('NaN')
                    if convert_to != '_mean':# ignore _mean
                        available_values.append(convert_to)

        # check if invalid values in  certain row
        # invalid_types = invalid_types_of_values = invalid_values = []
        invalid_types, invalid_types_of_values, invalid_values = ([] for i in range(3))
        for key, value in data[column_name].iteritems():
            if 'available_values' in column_info and value not in available_values and value not in invalid_values:
                invalid_values.append(value)

            if 'available_types' in column_info \
                    and type(column_info['available_types']) is list \
                    and any(column_info['available_types']) \
                    and type(value).__name__ not in column_info['available_types']:
                invalid_types_of_values.append(value)
                if type(value).__name__ not in invalid_types:
                    invalid_types.append(type(value).__name__)

        # if column_name == 'SOUTH':
        #     print data[column_name]
        #     print invalid_types_of_values
        #     print available_values
        #     sys.exit()



        # if there is a invalid value insert a message
        result[column_name] = []
        if invalid_values:
            msg_to_add = ' is an invalid value.'
            if len(invalid_values) > 1:
                msg_to_add = ' are invalid values.'
            result[column_name].append(str.implode(invalid_values,',',True) + msg_to_add)
        if invalid_types_of_values:
            # 'contains invalid types of values (8). int or float required. string is given.'
            msg = 'contains invalid types of values (' + str.implode(invalid_types_of_values, ',',True) + '). ' + str.implode(column_info['available_types'], ' or ') + ' required, ' + \
                  str.implode(invalid_types, ',') + ' given.'
            result[column_name].append(msg)
        if not invalid_values and not invalid_types_of_values:
            result[column_name] = True
        i += 1
    return result
