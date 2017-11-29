import numpy as np
import pandas as pd
import sys
import math
import str as mystr

class PreProcess:
    def __init__(self,df,columns_config):
        """Constructor of a :class:`PreProcess`.

            :param df: pandas dataframe which a user wants to preprocess.
            :param columns_config: Configuration of columns. It includes the configuration of
             which columns a user wants to extract, how to deal with empty columns,
             whether a user wants to apply one hot encoding, and so on.

             example:
             columns_config = {
                'column_1':{ # the column a user wants to extract from the data (df)
                    'conversion':{# values a user wants to convert. Requires dictionary.
                        # On the key (left), specify the value you want to convert from (convert_from).
                        # On the value (right), specify the value you want to convert to (convert_to).
                        'hello':'world'
                    },
                    one_hot_encoding : True # if this is true, apply one hot encodeling to the column
                },
                'column_2':{
                    'conversion':{
                        # if '_NaN' is specified to the key ('convert_from'), look for NaN and convert them to the value ('convert_to')
                        '_NaN': 0,

                        # jf '_mean' is specified to the value ('convert_to'), it will converts to mean value of the column.
                        '_NaN':'_mean'
                },
                'column_3'{

                },
                'diff_column_3_2'{
                    'recalculation':{# sometimes you may want recalculate value after you changed some values.
                                     # Then specify recalculation, For now, only subtraction is available.
                        'subtraction':[# subtracts the values of 'column_2' from 'column_3'.
                                       # if you specify like ['column_3', 'column_2', 'column_1'], it means subtract the values of 'column_2' and 'column_1' from 'column_3'.
                                       # ('column_3' - 'column_2' -'column_1')
                            ['column_3', 'column_2']
                        ]
                    }
                }
            }
    },
        """
        self.df = df
        self.columns_config = columns_config


    def convert_values_and_extract_data(self):
        """
        convert data in self.df according to self,columns_config
        """
        columns_to_extract = []
        mean = 0

        for column_name, column_info_2 in self.columns_config.items():

            # if there is a config of 'conversion' apply conversion
            if 'conversion' in column_info_2 \
                    and 'values' in column_info_2['conversion'] \
                    and  any(column_info_2['conversion']['values']):

                # To convert to mean, we firstly have to replace the numeric values with NaN,
                # then calculate mean
                for convert_from, convert_to in column_info_2['conversion']['values'].items():
                    for key, value in self.df[column_name].iteritems():
                        if convert_to != "_mean" and (
                            (convert_from == "_NaN" and pd.isnull(value)) or convert_from == value):
                            self.df.loc[key, column_name] = convert_to

                # if '_mean' is specified calculate mean of the column
                if '_mean' in column_info_2['conversion']['values'].values():
                    tmp_data = self.df.copy(deep=True)
                    for convert_from, convert_to in column_info_2['conversion']['values'].iteritems():
                        if convert_to == '_mean':
                            tmp_data[column_name] = tmp_data[column_name].replace(convert_from, np.NaN)
                    mean = self.average(tmp_data[column_name])

                # apply value conversion
                for convert_from, convert_to in column_info_2['conversion']['values'].items():
                    for key, value in self.df[column_name].iteritems():
                        if convert_to == "_mean" and (
                                convert_from == value or convert_from == '_NaN' and pd.isnull(value)):
                            self.df.loc[key, column_name] = mean

            columns_to_extract.append(column_name)

        self.df = self.df[columns_to_extract]


    def average(self,data_of_a_column):
        """
        :param data_of_a_column: requires a row of pandas dataframe such as self.df["column_1"]
        :return:  returns the column's average in float
        """
        sum = i = 0
        for key, value in data_of_a_column.iteritems():
            if isinstance(value, (int, np.integer, float)) and not math.isnan(value):
                sum += value
                i += 1
        return float(sum) / float(i)


    def recalculation(self):
        """
        Executes calculation usually after convert some values in a dataframe(self.df) according to self.columns_config,
        and insert the result into self.df.
        Currently, only subtraction is available. See the documentation which is on the top of this class.
        """
        for column_name, column_info in self.columns_config.items():
            if 'recalculation' in column_info and any(column_info['recalculation']):
                if 'subtraction' in column_info['recalculation'] \
                        and any(column_info['recalculation']['subtraction']):
                    i = 0
                    for column_name_2 in column_info['recalculation']['subtraction']:
                        if i == 0:
                            self.df[column_name] = self.df[column_name_2]
                        else:
                            self.df[column_name] = self.df[column_name] - self.df[column_name_2]
                        i += 1


    def set_one_hot_encoding_list(self):
        """
        Extracts the columns which a user wants to apply one hot encoding into a list, and store it to self.one_hot_encoding_list
        """
        self.one_hot_encoding_list = []
        for column_name, column_info in self.columns_config.items():
            if 'one_hot_encoding' in column_info and column_info['one_hot_encoding'] == True:
                self.one_hot_encoding_list.append(column_name)

    def apply_one_hot_encoding(self):
        """
        Applys one hot encoding to df's columns a user specified , and reflect them into self.df.

        """
        self.set_one_hot_encoding_list()
        self.df = pd.get_dummies(data=self.df, columns=self.one_hot_encoding_list)


    def are_valid_data(self):
        """
        Executes simple validation. It checks whether the values in each row are available value or valid types.
        :return dict result: result of each column's validation
        """
        result = {}
        i = 0
        for column_name, column_info in self.columns_config.items():
            available_values = []

            # if 'available_values' are set in column_info, the value in the self.df must be in the available_values
            if 'available_values' in column_info \
                    and type(column_info['available_values']) is list \
                    and any(column_info['available_values']):
                available_values.extend(column_info['available_values'])

                # store the value of convert_to to available_values
                if 'conversion' in column_info \
                        and column_info['conversion']['values'] \
                        and  any(column_info['conversion']['values']):
                    for convert_from, convert_to in column_info['conversion']['values'].items():
                        # if convert_to == '_NaN':  # if '_NaN', set NaN to convert_to
                        #     convert_to = float('NaN')
                        if convert_to != '_mean':  # ignore _mean
                            available_values.append(convert_to)

            # check if invalid values in  certain row
            # invalid_types = invalid_types_of_values = invalid_values = []
            invalid_types, invalid_types_of_values, invalid_values = ([] for i in range(3))
            for key, value in self.df[column_name].iteritems():
                if 'available_values' in column_info and value not in available_values and value not in invalid_values:
                    invalid_values.append(value)

                if 'available_types' in column_info \
                        and type(column_info['available_types']) is list \
                        and any(column_info['available_types']) \
                        and type(value).__name__ not in column_info['available_types']:
                    invalid_types_of_values.append(value)
                    if type(value).__name__ not in invalid_types:
                        invalid_types.append(type(value).__name__)




            # if there is a invalid value insert a message
            result[column_name] = []
            if invalid_values:
                msg_to_add = ' is an invalid value.'
                if len(invalid_values) > 1:
                    msg_to_add = ' are invalid values.'
                result[column_name].append(mystr.implode(invalid_values, ',', True) + msg_to_add)
            if invalid_types_of_values:
                # 'contains invalid types of values (8). int or float required. string is given.'
                msg = 'contains invalid types of values (' + mystr.implode(invalid_types_of_values, ',',
                                                                         True) + '). ' + mystr.implode(
                    column_info['available_types'], ' or ') + ' required, ' + \
                      mystr.implode(invalid_types, ',') + ' given.'
                result[column_name].append(msg)
            if not invalid_values and not invalid_types_of_values:
                result[column_name] = True
            i += 1
        return result
    # def validate_one_hot_encoding(self,one_hot_encoded_columns_list):
    #     one_hot_encoding_columns = []
    #     for column_name, config in self.columns_config.items():
    #         if 'one_hot_encoding' in config and config['one_hot_encoding']==True:
    #             for value in config['available_values']:
    #                 one_hot_encoding_columns.append(column_name + '_' + value)
    #
    #     print len(one_hot_encoding_columns)
        # sys.exit()
    def validate_one_hot_encoding(self):
        one_hot_encoding_columns = []
        for column_name, config in self.columns_config.items():

            if 'one_hot_encoding' in config and config['one_hot_encoding'] == True:
                available_values = []
                if 'available_values' in config \
                        and type(config['available_values']) is list \
                        and any(config['available_values']):
                    available_values.extend(config['available_values'])

                    # store the value of convert_to to available_values
                    if 'conversion' in config and any(config['conversion']):
                        for convert_from, convert_to in config['conversion'].items():
                            if convert_to != '_mean':  # ignore _mean
                                available_values.append(convert_to)
                if any(available_values):
                    for value in available_values:
                        # print value
                        one_hot_encoding_columns.append(column_name + '_' + str(value))

        print one_hot_encoding_columns
        print len(one_hot_encoding_columns)
        # sys.exit()