import unittest
import pandas as pd
import numpy as np
# sys.path.append('../sample.py')
import sys,os
sys.path.append(os.pardir)
import sample
import pre_process
from pandas.util.testing import assert_frame_equal
from collections import OrderedDict

import unittest
from unittest_data_provider import data_provider

#https://pypi.python.org/pypi/unittest-data-provider/1.0.0
# def data_provider(fn_data_provider):
#     """Data provider decorator, allows another callable to provide the data for the test"""
#     def test_decorator(fn):
#         def repl(self, *args):
#             for i in fn_data_provider():
#
#                 try:
#                     fn(self, *i)
#                 except AssertionError:
#                     print "Assertion error caught with data set ", i
#                     raise
#         return repl
#     return test_decorator

class TestPreProcess(unittest.TestCase):

    __data_for_test_convert_values_and_extract_data__return_expected_values = lambda:[
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 98,  np.NaN, 94 ], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 98,  np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            ),
            {
                'one':{
                    'conversion': {
                        98: '_mean',  # if "_mean" is specified to convert to give a average of  the column
                        '_NaN': 'mean',  # if '_NaN' is specified to convert from NaNs are converted to converted to
                        94: 'something'  # convert convert_from to convert to
                    }
                },
                'two': {

                }
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 1.5, 'mean','something'], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            )
        ]
    ]

    @data_provider(__data_for_test_convert_values_and_extract_data__return_expected_values)
    def test_convert_values_and_extract_data__return_expected_values(self, data, columns_info, expected):
        actual = pre_process.convert_values_and_extract_data(data, columns_info)
        assert_frame_equal(expected, actual, check_dtype = False, check_like = True)

    __data_for_test_average__return_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]) # returns valid average
                }
            ),
            'one',
            1.5
        ]
    ]

    @data_provider(__data_for_test_average__return_expected_values)
    def test_average__return_expected_values(self, data, column_name, expected):
        actual = pre_process.average(data[column_name])
        self.assertEquals(expected,actual)

    __data_for_test_average__return_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1])  # returns valid average
                }
            ),
            'one',
            1.5
        ]
    ]

    @data_provider(__data_for_test_average__return_expected_values)
    def test_average__return_expected_values(self, data, column_name, expected):
        actual = pre_process.average(data[column_name])
        self.assertEquals(expected, actual)

    __data_for_test_average__raises_valid_exception = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series(['str'], index=[0])  # returns valid exception
                }
            ),
            'one',
        ]
    ]

    @data_provider(__data_for_test_average__raises_valid_exception)
    def test_average__raises_valid_exception(self, data, column_name):
        try:
            actual = pre_process.average(data[column_name])
            assert False
        except ZeroDivisionError:
            assert True


    __data_for_test_recalculation__return_expected_values = lambda: [
        # return expected value when number of columns specified in subtraction is two
        [
           pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'two_one_diff': pd.Series([0, 0], index=[0, 1])
                }
            ),
            {
                'two_one_diff':{
                    'recalculation': {
                        'subtraction': ['two','one']
                    }
                }
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'two_one_diff': pd.Series([1, 1], index=[0, 1])
                }
            )
        ],
        # return expected value when number of columns specified in subtraction is three
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1]),
                    'three_two_one_diff': pd.Series([0, 0], index=[0, 1])
                }
            ),
            {
                'three_two_one_diff': {
                    'recalculation': {
                        'subtraction': ['three','two', 'one']
                    }
                }
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1]),
                    'three_two_one_diff': pd.Series([1, -1], index=[0, 1])
                }
            )
        ],
        # when recalculation is not specified, returns same data
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1]),
                    'three_two_one_diff': pd.Series([0, 0], index=[0, 1])
                }
            ),
            {
                'three_two_one_diff': {
                }
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1]),
                    'three_two_one_diff': pd.Series([0, 0], index=[0, 1])
                }
            )
        ],
        # when subtraction  is not specified, returns same data
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1]),
                    'three_two_one_diff': pd.Series([0, 0], index=[0, 1])
                }
            ),
            {
                'three_two_one_diff': {
                    'recalculation': {
                    }
                }
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1]),
                    'three_two_one_diff': pd.Series([0, 0], index=[0, 1])
                }
            )
        ],
        # when subtraction is empty, returns same data
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1]),
                    'three_two_one_diff': pd.Series([0, 0], index=[0, 1])
                }
            ),
            {
                'three_two_one_diff': {
                    'recalculation': {
                        'subtraction':{

                        }
                    }
                }
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]),
                    'two': pd.Series([2, 3], index=[0, 1]),
                    'three': pd.Series([4, 4], index=[0, 1]),
                    'three_two_one_diff': pd.Series([0, 0], index=[0, 1])
                }
            )
        ]
    ]

    @data_provider(__data_for_test_recalculation__return_expected_values)
    def test_recalculation__return_expected_values(self, data, columns_info, expected):
        actual = pre_process.recalculation(data,columns_info)
        assert_frame_equal(expected, actual,check_dtype = False, check_like = True)

    __data_for_test_get_one_hot_encode_list___returns_expected_values = lambda: [
        [
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

    @data_provider(__data_for_test_get_one_hot_encode_list___returns_expected_values)
    def test_get_one_hot_encode_list__returns_expected_values(self, columns_info, expected):
        actual = pre_process.get_one_hot_encode_list(columns_info)
        self.assertListEqual(expected, actual)

    __data_for_test_apply_one_hot_encode___returns_expected_values = lambda: [
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

    @data_provider(__data_for_test_apply_one_hot_encode___returns_expected_values)
    def test_apply_one_hot_encode__returns_expected_values(self, data, columns_info, expected):
        actual = pre_process.apply_one_hot_encode(data, columns_info)
        assert_frame_equal(expected, actual, check_dtype = False, check_like = True)

    __data_for_test_are_valid_data___returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([2, 4, 5], index=[0, 1, 2]),
                    'three': pd.Series([4, 9, 13], index=[0, 1, 2]),
                    'four': pd.Series(['8'], index=[0]),
                    'five': pd.Series(['8', '16'], index=[0, 1]),
                    'six': pd.Series([9, '16', 32], index=[0,1,2]),
                    'seven': pd.Series([8, 16, 94], index=[0, 1, 2])
                }
            ),
            OrderedDict([
                ('one', {'available_values': [
                    1,2,3
                ]}),
                ('two', {'available_values': [
                    2,4,6
                ]}),
                ('three', {'available_values': [
                    4, 8, 12
                ]}),
                ('four', {
                    'available_types': ['int', 'float']
                }),
                ('five', {
                    'available_types': ['int', 'float']
                }),
                ('six', {
                    'available_values': [
                        8, 16, 32
                    ],
                    'available_types': ['int', 'float']
                }),
                ('seven', {
                    'conversion':{
                        '_NaN':94
                    },
                    'available_values': [
                        8, 16
                    ]
                }),
            ]),
            {
                'one': True, # returns true is all values are valid
                'two': ['5 is an invalid value.'], #returns expected value if there is an invalid value
                'three': ['9,13 are invalid values.'],  # returns expected value if there are are multiple invalid value
                'four': ['contains invalid types of values ("8"). int or float required, str given.'],# returns expected value if there is an invalid types of value
                'five': ['contains invalid types of values ("8","16"). int or float required, str given.'],# returns expected value if there are multiple invalid types of value
                'six': ['9,"16" are invalid values.', 'contains invalid types of values ("16"). int or float required, str given.'],#returns expected value if there are  invalid value and  invalid types of values
                'seven':True
            },
        ]
    ]

    @data_provider(__data_for_test_are_valid_data___returns_expected_values)
    def test_are_valid_data__returns_expected_values(self, data, columns_info, expected):
        # print data
        # sys.exit()
        actual = pre_process.are_valid_data(data, columns_info)
        self.assertDictEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()

