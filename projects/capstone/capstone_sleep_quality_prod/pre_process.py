import numpy as np
import pandas as pd
import sys
import math
import re
import scipy.stats as ss
pd.options.mode.chained_assignment = None

class PreProcess:
    def __init__(self,df,columns_config):
        """Constructor of a :class:`PreProcess`.

            :param df: pandas dataframe which a user wants to preprocess.
            :param columns_config: Configuration of columns. It includes the configuration of
             which columns a user wants to extract, how to deal with empty columns,
             whether a user wants to apply one hot encoding, and so on.

             example:
             columns_config = {
                'column_1':{ # A name of the column a user wants to extract from the data (df)
                    'conversion':{
                        'values':[# Values a user wants to convert. Requires dictionary.
                            # On the key (left), specify the value you want to convert from.
                            # On the value (right), specify the value you want to convert to.
                            'hello':'world'
                        ]
                    },
                    one_hot_encoding : True # if this is true, apply one-hot encoding to the column
                },
                'column_2':{
                    'conversion':{
                        'values'[
                            # if '_NaN' is specified to the key, it looks for NaN and converts them to the value on the right.
                            '_NaN': 0,
                            # jf '_mean' is specified to the value, it will converts to mean value of the column.
                            '_NaN':'_mean'
                        ],
                        # True if you want to apply logistic transformation to this column's values
                        'log_trans': True,
                        # if astype specified, it converts the type of columns to the type you specified
                        'astype': 'int64'
                },
                'column_3'{

                }
            }
    },
        """
        self.df = df
        self.columns_config = columns_config


    def extract_data(self):
        """
        Extracts all the columns from the dataset(self.df) according to self.columns_config a user specified
        """
        columns_to_extract = self.columns_config.keys()
        self.df = self.df[columns_to_extract]

    def average(self,data_of_a_column):
        """
        :param data_of_a_column: Requires a column of pandas dataframe such as self.df["column_1"]
        :return:  Returns the column's average in float.
        """
        sum = i = 0
        for key, value in data_of_a_column.iteritems():
            if isinstance(value, (np.integer, float)) and not math.isnan(value):
                sum += value
                i += 1
        return float(sum) / float(i)

    def set_one_hot_encoding_list(self):
        """
        Extracts the columns which a user wants to apply one hot encoding into a list and stores it to self.one_hot_encoding_list
        """
        self.one_hot_encoding_list = []
        for column_name, column_info in self.columns_config.items():
            if 'one_hot_encoding' in column_info and column_info['one_hot_encoding'] == True:
                self.one_hot_encoding_list.append(column_name)

    def apply_one_hot_encoding(self):
        """
        Applys one-hot encoding to self.df's columns according to self.columns_config

        """
        self.set_one_hot_encoding_list()
        self.df = pd.get_dummies(data=self.df, columns=self.one_hot_encoding_list)

    def set_target_column_names(self):
        """
        Finds target variables from self.columns_config and stores the column names to self.target_column_names
        """
        self.target_column_names = []
        for column_name, column_config in self.columns_config.iteritems():
            if  'is_target_variable' in column_config and column_config['is_target_variable'] == True:
                self.target_column_names.append(column_name)

    def get_inputs_and_outputs(self):
        """
        Divides input and output variables and returns them.
        :return: Input and output variables in pandas dataframe.
        """
        self.set_target_column_names()
        return self.df.drop(self.target_column_names, axis=1),self.df[self.target_column_names]


    def drop_columns_by_regexp(self,patterns):
        """
        Drops matched columns by regular expressions from self.df
        :param patterns: The regular expressions for column names which users wish to drop.
        """
        matched_column_names = self.get_matched_column_names(patterns)
        self.df.drop(matched_column_names, axis=1,inplace=True)

    def get_matched_column_names(self,patterns):
        """
        Gets matched columns from self.df by regular expressions.
        :param patterns: The regular expressions for column names.
        :return matched_column_names: Matched column names in a list by regular expressions.
        """
        matched_column_names = []
        for pattern in patterns:
            for column_name in list(self.df):
                if re.search(pattern, column_name):
                    matched_column_names.append(column_name)
        return matched_column_names

    def get_column_names_to_apply_log_trans(self):
        """
        Gets column names which users wish to apply log transformation
        :return: column_names_to_apply_log_trans: A list of column names which users wish to apply log transformation
        """
        column_names_to_apply_log_trans = []
        for column_name,config in self.columns_config.items():
            if 'conversion' in config \
                and 'log_trans' in config['conversion'] \
                and config['conversion']['log_trans'] == True:
                column_names_to_apply_log_trans.append(column_name)
        return column_names_to_apply_log_trans


    def apply_log_trans_according_to_columns_config(self):
        """
        Applys log transformation to self.df accoording to self.columns_config
        """
        columns_to_apply = self.get_column_names_to_apply_log_trans()
        self.apply_log_trans(columns_to_apply)

    def apply_log_trans(self,columns_to_apply):
        """
        Applys log transformation to columns a user specified
        :param columns_to_apply:
        """
        # columns_to_apply = self.get_column_names_to_apply_log_trans()
        self.df[columns_to_apply] = self.df[columns_to_apply].apply(lambda x: np.log(x + 1))


    def convert_values(self):
        """
        Converts values in self,df according to self.columns_config
        """
        mean = 0
        for column_name, column_info_2 in self.columns_config.items():

            # if there is a config of 'conversion' apply conversion
            if 'conversion' in column_info_2:
                if 'values' in column_info_2['conversion'] \
                    and  any(column_info_2['conversion']['values']):

                    #Converting values except for "_mean"
                    for convert_from, convert_to in column_info_2['conversion']['values'].items():
                        for key, value in self.df[column_name].iteritems():
                            if convert_to != "_mean" and (
                                (convert_from == "_NaN" and pd.isnull(value)) or convert_from == value):
                                self.df.loc[key, column_name] = convert_to

                    # if '_mean' is specified, calculates the mean of the column
                    if '_mean' in column_info_2['conversion']['values'].values():
                        tmp_data = self.df.copy(deep=True)
                        for convert_from, convert_to in column_info_2['conversion']['values'].iteritems():
                            if convert_to == '_mean':
                                tmp_data[column_name] = tmp_data[column_name].replace(convert_from, np.NaN)
                        mean = self.average(tmp_data[column_name])

                    # Insert the mean to the specified values.
                    for convert_from, convert_to in column_info_2['conversion']['values'].items():
                        for key, value in self.df[column_name].iteritems():
                            if convert_to == "_mean" and (
                                    convert_from == value or convert_from == '_NaN' and pd.isnull(value)):
                                self.df.loc[key, column_name] = mean

    def convert_types(self):
        """
        Converts types of the columns in self,df according to self.columns_config
        """
        for column_name, column_info_2 in self.columns_config.items():
            # if there is a config of 'conversion' apply conversion
            if 'conversion' in column_info_2:
                if 'astype' in column_info_2['conversion'] \
                        and column_info_2['conversion']['astype']:
                    self.df[column_name] = self.df[column_name].astype(column_info_2['conversion']['astype'])


    def get_column_names_contain_continuous_values(self):
        """
        Gets column names contain continuous values.
        :return: column_names_contain_continuous_values: A list of column names contain continuous values
        """
        column_names_contain_continuous_values = []
        for column_name, config in self.columns_config.items():
            if 'continuous' in config \
                    and config['continuous'] == True:
                column_names_contain_continuous_values.append(column_name)
        return column_names_contain_continuous_values

    def get_skews(self,with_column_names=True):
        """
        Gets each skew of continuous variables.
        :param with_column_names: If this is true, returns a pandaframes' series which has column names as indexes and skews as values
        :return: A list of skews or pandaframes' series which has column names as index and skews as values
        """
        column_names_contain_continuous_values = self.get_column_names_contain_continuous_values()
        skews = []
        for column_name in column_names_contain_continuous_values:
            skews.append(ss.skew(self.df[column_name]))
        if with_column_names == True:
            skews_with_column_names = pd.Series(data=skews, index=column_names_contain_continuous_values)
            skews_with_column_names.sort_values(ascending=False, inplace=True)
            return skews_with_column_names
        else:
            return skews

    def check_if_columns_contain_negative_values(self):
        """
        Checks if continuous columns have negative values or not
        :return:  A pandas series which has column names as indexes and result as values
        """
        column_names_contain_continuous_values = self.get_column_names_contain_continuous_values()
        return (self.df[column_names_contain_continuous_values] < 0).any()

    def raise_values_to_positive(self,min = 1):
        """
        Raises negative continuous columns' values to positive
        :param min: The minimum values when it raises negative values to positive.
        """
        check_negative_values_result = self.check_if_columns_contain_negative_values()
        columns_to_raise = []
        for column_name, value in check_negative_values_result.iteritems():
            if value == True:
                self.df[column_name] += abs(self.df[column_name].min()) + min

    def set_log_trans_based_on_skewness(self,allowed_skew):
        """
        Sets "'log trans' = True" to self.columns_config based on skews
        :param allowed_skew: A maximum absolute skew which does not require log transformation.
        """
        skews = self.get_skews()
        skews = skews.abs()
        for column_name, value in skews.iteritems():
            if value > allowed_skew:
                if 'conversion' not in self.columns_config[column_name]:
                    self.columns_config[column_name]['conversion'] = {}
                if 'log_trans' not in self.columns_config[column_name]['conversion']:
                    self.columns_config[column_name]['conversion']['log_trans'] = None
                self.columns_config[column_name]['conversion']['log_trans'] = True
