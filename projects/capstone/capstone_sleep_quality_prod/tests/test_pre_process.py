import pandas as pd
import numpy as np
import sys,os
sys.path.append(os.pardir)
sys.path.append('../lib')
import pre_process
from pandas.util.testing import assert_frame_equal,assert_series_equal
import unittest
from unittest_data_provider import data_provider



class TestPreProcess(unittest.TestCase):

    # python test_pre_process.py TestPreProcess.test__init____set_expected_properties
    __data_for_test__init____set_expected_properties = lambda :[
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2])
                }
            ),
            {
                'one':{},
                'two':{}
            },
        ]
    ]

    @data_provider(__data_for_test__init____set_expected_properties)
    def test__init____set_expected_properties(self,df,columns_config):
        expected_1 = df
        expected_2 = columns_config

        pre_process_1 = pre_process.PreProcess(df,columns_config)

        actual_1 = getattr(pre_process_1, "df")
        actual_2 = getattr(pre_process_1, "columns_config")

        assert_frame_equal(expected_1, actual_1, check_dtype=False, check_like=True)
        self.assertDictEqual(expected_2, actual_2)




    # python test_pre_process.py TestPreProcess.test_extract_data__sets_expected_values
    __data_for_test_extract_data__sets_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 1, 2, 3], index=[0, 1, 2, 3]),
                    'two': pd.Series([1, 1, 2, 3], index=[0, 1, 2, 3]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2])
                }
            ),
            {
                'one': {
                    'continuous': True
                },
                'two': {
                    'continuous': True
                },
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 1, 2, 3], index=[0, 1, 2, 3]),
                    'two': pd.Series([1, 1, 2, 3], index=[0, 1, 2, 3]),
                }
            ),
        ],
    ]

    @data_provider(__data_for_test_extract_data__sets_expected_values)
    def test_extract_data__sets_expected_values(self, df, columns_config,expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.extract_data()
        actual = pre_process_1.df
        assert_frame_equal(expected, actual,check_like=True)




    # python test_pre_process.py TestPreProcess.test_average__returns_expected_values
    __data_for_test_average__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]) # returns valid average
                }
            ),
            {
                'one': {}
            },
            'one',
            1.5
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1.0, 2.0], index=[0, 1])  # returns valid average
                }
            ),
            {
                'one': {}
            },
            'one',
            1.5
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1.0, 2.0, float('NaN')], index=[0, 1, 2])  # returns valid average
                }
            ),
            {
                'one': {}
            },
            'one',
            1.5
        ],
    ]

    @data_provider(__data_for_test_average__returns_expected_values)
    def test_average__returns_expected_values(self, df, columns_config, column_name, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        actual = pre_process_1.average(df[column_name])
        self.assertEquals(expected,actual)




    __data_for_test_average__raises_valid_exception = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series(['str'], index=[0])  # returns valid exception
                }
            ),
            {
                'one': {},
                'two': {}
            },
            'one',
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([float('NaN')], index=[0])  # returns valid exception
                }
            ),
            {
                'one': {},
                'two': {}
            },
            'one',
        ]
    ]

    @data_provider(__data_for_test_average__raises_valid_exception)
    def test_average__raises_valid_exception(self, df, columns_config, column_name):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        try:
            actual = pre_process_1.average(df[column_name])
            assert False
        except ZeroDivisionError:
            assert True




    # python test_pre_process.py TestPreProcess.test_set_one_hot_encoding_list__sets_expected_values
    __data_for_test_set_one_hot_encoding_list__sets_expected_values = lambda: [
        [
            pd.DataFrame({}),
            {
                'one':{
                    'one_hot_encoding':True
                },
                'two': {
                    'one_hot_encoding': False
                },
                'three': {
                },
            },
            ['one']
        ]
    ]

    @data_provider(__data_for_test_set_one_hot_encoding_list__sets_expected_values)
    def test_set_one_hot_encoding_list__sets_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.set_one_hot_encoding_list()
        actual = pre_process_1.one_hot_encoding_list
        self.assertListEqual(expected, actual)




    # python test_pre_process.py TestPreProcess.test_apply_one_hot_encoding__sets_expected_values
    __data_for_test_apply_one_hot_encoding__sets_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1])
                }
            ),
            {
                'one': {
                    'one_hot_encoding': True
                },
                'two': {
                    'one_hot_encoding': False
                },
                'three': {
                },
            },
            pd.DataFrame(
                {
                    'one_1': pd.Series([1, 0], index=[0, 1]),
                    'one_2': pd.Series([0, 1], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1])
                }
            ),
        ]
    ]

    @data_provider(__data_for_test_apply_one_hot_encoding__sets_expected_values)
    def test_apply_one_hot_encoding__sets_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.apply_one_hot_encoding()
        actual = pre_process_1.df
        assert_frame_equal(expected, actual, check_dtype=False, check_like=True)




    # python test_pre_process.py TestPreProcess.test_set_target_column_names__sets_expected_values
    __data_for_test_set_target_column_names__sets_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'three': {
                    'is_target_variable': True

                },
            },
            ['three']
        ],
        [
            pd.DataFrame(
                {
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'three': {
                    'is_target_variable': False
                },
            },
            []
        ],
        [
            pd.DataFrame(
                {
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'three': {
                },
            },
            []
        ]
    ]

    @data_provider(__data_for_test_set_target_column_names__sets_expected_values)
    def test_set_target_column_names__sets_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.set_target_column_names()
        actual = pre_process_1.target_column_names
        self.assertListEqual(expected, actual)




    # python test_pre_process.py TestPreProcess.test_get_inputs_and_outputs__returns_expected_values
    __data_for_test_get_inputs_and_outputs__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                },
                'two': {
                },
                'three': {
                    'is_target_variable': True

                },
                'four': {
                    'is_target_variable': False
                },
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            pd.DataFrame(
                {
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            )

        ]
    ]
    @data_provider(__data_for_test_get_inputs_and_outputs__returns_expected_values)
    def test_get_inputs_and_outputs__returns_expected_values(self, df, columns_config, expected_1, expected_2):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        actual_1, actual_2 = pre_process_1.get_inputs_and_outputs()
        assert_frame_equal(expected_1, actual_1, check_dtype=False, check_like=True)
        assert_frame_equal(expected_2, actual_2, check_dtype=False, check_like=True)




    # python test_pre_process.py TestPreProcess.test_drop_columns_by_regexp__sets_expected_values
    __data_for_test_drop_columns_by_regexp__sets_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two_94': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three_96': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {

                },
                'two': {
                    'one_hot_encoding': True,
                },
                'three':{
                    'one_hot_encoding': True,
                }
            },
            ['94$','96$'],
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),

        ]
    ]
    @data_provider(__data_for_test_drop_columns_by_regexp__sets_expected_values)
    def test_drop_columns_by_regexp__sets_expected_values(self, df, columns_config, patterns, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.drop_columns_by_regexp(patterns)
        actual = pre_process_1.df
        assert_frame_equal(expected, actual, check_dtype=False, check_like=True)




    # python test_pre_process.py TestPreProcess.test_get_matched_column_names__returns_expected_values
    __data_for_test_get_matched_column_names__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two_94': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three_96': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            ['94$', '96$'],
            ['two_94','three_96']
        ]
    ]

    @data_provider(__data_for_test_get_matched_column_names__returns_expected_values)
    def test_get_matched_column_names__returns_expected_values(self, df, patterns, expected):
        pre_process_1 = pre_process.PreProcess(df, patterns)
        actual = pre_process_1.get_matched_column_names(patterns)
        self.assertListEqual(expected, actual)




    # python test_pre_process.py TestPreProcess.test_get_column_names_to_apply_log_trans__returns_expected_values
    __data_for_test_get_column_names_to_apply_log_trans__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'five': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'conversion': {
                        'log_trans':True
                    },
                },
                'two': {
                    'conversion': {
                        'log_trans': True
                    },
                },
                'three':{
                    'conversion':{
                        'log_trans': False
                    },
                },
                'four': {
                    'conversion': {

                    },
                },
                'five': {

                }


            },
            ['one', 'two']
        ]
    ]

    @data_provider(__data_for_test_get_column_names_to_apply_log_trans__returns_expected_values)
    def test_get_column_names_to_apply_log_trans__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        actual = pre_process_1.get_column_names_to_apply_log_trans()
        self.assertItemsEqual(expected, actual)




    # python test_pre_process.py TestPreProcess.test_apply_log_trans_according_to_columns_config__sets_expected_values
    __data_for_test_apply_log_trans_according_to_columns_config__sets_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'five': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'conversion': {
                        'log_trans': True
                    },
                },
                'two': {
                    'conversion': {
                        'log_trans': True
                    },
                },
                'three': {
                    'conversion': {
                        'log_trans': False
                    },
                },
                'four': {
                    'conversion': {

                    },
                },
                'five': {

                }

            },
            pd.DataFrame(
                {
                    'one': pd.Series([0.693147, 1.098612, 1.386294], index=[0, 1, 2]),
                    'two': pd.Series([0.693147, 1.098612, 1.386294], index=[0, 1, 2]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'five': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
        ]
    ]

    @data_provider(__data_for_test_apply_log_trans_according_to_columns_config__sets_expected_values)
    def test_apply_log_trans_according_to_columns_config__sets_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.apply_log_trans_according_to_columns_config()
        actual = pre_process_1.df
        assert_frame_equal(expected, actual)




    # python test_pre_process.py TestPreProcess.test_apply_log_trans__sets_expected_values
    __data_for_test_apply_log_trans__sets_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                },
                'two': {
                },
                'three': {
                },


            },
            ['one','two'],
            pd.DataFrame(
                {
                    'one': pd.Series([0.693147, 1.098612, 1.386294], index=[0, 1, 2]),
                    'two': pd.Series([0.693147, 1.098612, 1.386294], index=[0, 1, 2]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
        ]
    ]

    @data_provider(__data_for_test_apply_log_trans__sets_expected_values)
    def test_apply_log_trans__sets_expected_values(self, df, columns_config, columns_to_apply, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.apply_log_trans(columns_to_apply)
        actual = pre_process_1.df
        assert_frame_equal(expected, actual)




    # python test_pre_process.py TestPreProcess.test_convert_values__sets_expected_values
    __data_for_test_convert_values__sets_expected_values = lambda:[
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 98,  np.NaN, 94 ], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, np.NaN, np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'three': pd.Series([1, 2, 3, 4], index=[0, 1, 2, 3]),

                    'four': pd.Series([1, 2, 98,  np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'five': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            ),
            {
                'one':{
                    'conversion': {
                        'values':{
                            98: '_mean',  # if "_mean" is specified to 'convert_to' give a average of  the column
                            '_NaN': 'mean',  # if '_NaN' is specified to 'convert_from' NaNs are converted to 'converted_to'
                            94: 'something'  # convert convert_from to convert to
                        }
                    }
                },
                'two': {
                    'conversion': {
                        'values': {
                            '_NaN': '_mean',
                            94: 'something'
                        }
                    }
                },
                'three':{
                    'conversion': {
                        'values': {
                            1: 4,
                            2: 3,
                            3: 2,
                            4: 1
                        }
                    }
                },
                'four':{

                },
                'five': {
                    'conversion': {
                        'values': {}
                    }
                }
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 1.5, 'mean','something'], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 1.5, 1.5, 'something'], index=[0, 1, 2, 3, 4]),
                    'three': pd.Series([4, 3, 2, 1], index=[0, 1, 2, 3]),
                    'four': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'five': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            )
        ]
    ]

    @data_provider(__data_for_test_convert_values__sets_expected_values)
    def test_convert_values__sets_expected_values(self, data, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(data, columns_config)
        pre_process_1.convert_values()
        actual = getattr(pre_process_1, "df")
        assert_frame_equal(expected, actual, check_dtype = False, check_like = True)




    # python test_pre_process.py TestPreProcess.test_convert_types__sets_expected_values
    __data_for_test_convert_types__sets_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1.1,2.1,3.1,4.1,5.1], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'three': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            ),
            {
                'one':{
                    'conversion': {
                        'astype': 'int64'
                    }
                },
                'two': {

                },
                'three': {
                    'conversion': {
                        'values': {}
                    }
                }
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3, 4, 5], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'three': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            )
        ]
    ]

    @data_provider(__data_for_test_convert_types__sets_expected_values)
    def test_convert_types__sets_expected_values(self, data, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(data, columns_config)
        pre_process_1.convert_types()
        actual = getattr(pre_process_1, "df")
        assert_frame_equal(expected, actual, check_dtype=True, check_like=True)




    # python test_pre_process.py TestPreProcess.test_get_column_names_contain_continuous_values__returns_expected_values
    __data_for_test_get_column_names_contain_continuous_values__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'continuous': True
                },
                'two': {
                    'continuous': True
                },
                'three': {

                },
                'four': {
                    'continuous': False
                },
            },
            ['one', 'two']
        ]
    ]

    @data_provider(__data_for_test_get_column_names_contain_continuous_values__returns_expected_values)
    def test_get_column_names_contain_continuous_values__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        actual = pre_process_1.get_column_names_contain_continuous_values()
        self.assertItemsEqual(expected, actual)




    # python test_pre_process.py TestPreProcess.test_get_skews__returns_expected_values
    __data_for_test_get_skews__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 1, 2, 3], index=[0, 1, 2, 3]),
                    'two': pd.Series([1, 2, 3, 3], index=[0, 1, 2, 3]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'continuous': True
                },
                'two': {
                    'continuous': True
                },
                'three': {

                },
                'four': {
                    'continuous': False
                },
            },
            True,
            pd.Series(
                {
                    'one': 0.49338220021815865,
                    'two': -0.49338220021815865
                }
            )
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 1, 2, 3], index=[0, 1, 2, 3]),
                    'two': pd.Series([1, 2, 3, 3], index=[0, 1, 2, 3]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'continuous': True
                },
                'two': {
                    'continuous': True
                },
                'three': {

                },
                'four': {
                    'continuous': False
                },
            },
            False,
            [0.49338220021815865, -0.49338220021815865]
        ],
    ]

    @data_provider(__data_for_test_get_skews__returns_expected_values)
    def test_get_skews__returns_expected_values(self, df, columns_config, with_column_names, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        actual = pre_process_1.get_skews(with_column_names)
        if with_column_names == True:
            assert_series_equal(expected, actual)
        else:
            self.assertItemsEqual(expected, actual)




    # python test_pre_process.py TestPreProcess.test_check_if_columns_contain_negative_values__returns_expected_values
    __data_for_test_check_if_columns_contain_negative_values__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([-1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'continuous': True
                },
                'two': {
                    'continuous': True
                },
                'three': {

                },
                'four': {
                    'continuous': False
                },
            },
            pd.Series(
                {
                    'one': True,
                    'two': False
                }
            )
        ]
    ]

    @data_provider(__data_for_test_check_if_columns_contain_negative_values__returns_expected_values)
    def test_check_if_columns_contain_negative_values__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        actual = pre_process_1.check_if_columns_contain_negative_values()
        self.assertItemsEqual(expected, actual)




    # python test_pre_process.py TestPreProcess.test_raise_values_to_positive__sets_expected_values
    __data_for_test_raise_values_to_positive__sets_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([-1, 0, 1], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three': pd.Series([-1, 0, 1], index=[0, 1, 2]),
                    'four': pd.Series([-1, 0, 1], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'continuous': True
                },
                'two': {
                    'continuous': True
                },
                'three': {

                },
                'four': {
                    'continuous': False
                },
            },
            1,
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'three': pd.Series([-1, 0, 1], index=[0, 1, 2]),
                    'four': pd.Series([-1, 0, 1], index=[0, 1, 2]),
                }
            ),
        ]
    ]

    @data_provider(__data_for_test_raise_values_to_positive__sets_expected_values)
    def test_raise_values_to_positive__sets_expected_values(self, df, columns_config,min, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.raise_values_to_positive(min)
        actual = pre_process_1.df
        assert_frame_equal(expected, actual)




    # python test_pre_process.py TestPreProcess.test_set_log_trans_based_on_abs_skew__returns_expected_values
    __data_for_test_set_log_trans_based_on_abs_skew__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 1, 2, 3], index=[0, 1, 2, 3]),
                    'two': pd.Series([1, 1, 2, 3], index=[0, 1, 2, 3]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'continuous': True
                },
                'two': {
                    'continuous': True,
                    'conversion': {
                        'log_trans': None
                    }
                },
                'three': {

                },
                'four': {
                    'continuous': False
                },
            },
            0.49,
            {
                'one': {
                    'continuous': True,
                    'conversion':{
                        'log_trans': True
                    }
                },
                'two': {
                    'continuous': True,
                    'conversion':{
                        'log_trans': True
                    }
                },
                'three': {

                },
                'four': {
                    'continuous': False
                },
            },
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 1, 2, 3], index=[0, 1, 2, 3]),
                    'two': pd.Series([1, 2, 3, 3], index=[0, 1, 2, 3]),
                    'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'continuous': True
                },
                'two': {
                    'continuous': True
                },
                'three': {

                },
                'four': {
                    'continuous': False
                },
            },
            0.50,
            {
                'one': {
                    'continuous': True
                },
                'two': {
                    'continuous': True,
                },
                'three': {

                },
                'four': {
                    'continuous': False
                },
            },
        ]
    ]

    @data_provider(__data_for_test_set_log_trans_based_on_abs_skew__returns_expected_values)
    def test_set_log_trans_based_on_abs_skew__returns_expected_values(self, df, columns_config, allowed_abs_skew,  expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.set_log_trans_based_on_abs_skew(allowed_abs_skew)
        actual = pre_process_1.columns_config
        self.assertDictEqual(expected, actual)




if __name__ == "__main__":
    unittest.main()

