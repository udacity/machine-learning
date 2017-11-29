import pandas as pd
import numpy as np
import sys,os
sys.path.append(os.pardir)
import sample
import pre_process
from pandas.util.testing import assert_frame_equal
from collections import OrderedDict
import unittest
from unittest_data_provider import data_provider


class TestPreProcess(unittest.TestCase):

    __data_for_test__init____set_valid_properties = lambda :[
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

    @data_provider(__data_for_test__init____set_valid_properties)
    def test__init____set_valid_properties(self,df,columns_config):
        expected_1 = df
        expected_2 = columns_config

        pre_process_1 = pre_process.PreProcess(df,columns_config)

        actual_1 = getattr(pre_process_1, "df")
        actual_2 = getattr(pre_process_1, "columns_config")

        assert_frame_equal(expected_1, actual_1, check_dtype=False, check_like=True)
        self.assertDictEqual(expected_2, actual_2)



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
    def test_convert_values_and_extract_data__return_expected_values(self, data, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(data, columns_config)
        pre_process_1.convert_values_and_extract_data()
        actual = getattr(pre_process_1, "df")
        assert_frame_equal(expected, actual, check_dtype = False, check_like = True)




    __data_for_test_average__return_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2], index=[0, 1]) # returns valid average
                }
            ),
            {
                'one': {},
                'two': {}
            },
            'one',
            1.5
        ],

    ]

    @data_provider(__data_for_test_average__return_expected_values)
    def test_average__return_expected_values(self, df, columns_config, column_name, expected):
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
    def test_recalculation__return_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.recalculation()
        actual = pre_process_1.df
        assert_frame_equal(expected, actual,check_dtype = False, check_like = True)

    __data_for_test_set_one_hot_encoding_list___returns_expected_values = lambda: [
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

    @data_provider(__data_for_test_set_one_hot_encoding_list___returns_expected_values)
    def test_set_one_hot_encoding_list__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.set_one_hot_encoding_list()
        actual = pre_process_1.one_hot_encoding_list
        self.assertListEqual(expected, actual)

    __data_for_test_apply_one_hot_encoding___returns_expected_values = lambda: [
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

    @data_provider(__data_for_test_apply_one_hot_encoding___returns_expected_values)
    def test_apply_one_hot_encoding__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.apply_one_hot_encoding()
        actual = pre_process_1.df
        assert_frame_equal(expected, actual, check_dtype = False, check_like = True)

    __data_for_test_are_valid_data___returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                    'two': pd.Series([1, 2, 4], index=[0, 1, 2]),
                    'three': pd.Series([1, 4, 5], index=[0, 1, 2]),
                    'four': pd.Series(['1'], index=[0]),
                    'five': pd.Series(['1', '2'], index=[0, 1]),
                    'six': pd.Series([4, '2', 3], index=[0,1,2]),
                    'seven': pd.Series([1, 2, 94], index=[0, 1, 2])
                }
            ),

            {
                'one':{
                    'available_values': [
                        1, 2, 3
                    ]
                },
                'two':{
                    'available_values': [
                        1, 2, 3
                    ]
                },

                'three':{
                    'available_values': [
                        1, 2, 3
                    ]
                },
                'four':{
                    'available_types': ['int', 'float']
                },
                'five': {
                    'available_types': ['int', 'float']
                },
                'six':{
                    'available_values': [
                        1, 2, 3
                    ],
                    'available_types': ['int', 'float']
                },
                'seven':{
                    'conversion': {
                        '_NaN': 94
                    },
                    'available_values': [
                        1, 2
                    ]
                },
            },
            # OrderedDict([
            #     ('one', {'available_values': [
            #         1,2,3
            #     ]}),
            #     ('two', {'available_values': [
            #         1,2,3
            #     ]}),
            #     ('three', {'available_values': [
            #         1, 2, 3
            #     ]}),
            #     ('four', {
            #         'available_types': ['int', 'float']
            #     }),
            #     ('five', {
            #         'available_types': ['int', 'float']
            #     }),
            #     ('six', {
            #         'available_values': [
            #             1, 2, 3
            #         ],
            #         'available_types': ['int', 'float']
            #     }),
            #     ('seven', {
            #         'conversion':{
            #             '_NaN':94
            #         },
            #         'available_values': [
            #             1, 2
            #         ]
            #     }),
            #
            # ]),
            {
                'one': True, # returns true is all values are valid
                'two': ['4 is an invalid value.'], #returns expected value if there is an invalid value
                'three': ['4,5 are invalid values.'],  # returns expected value if there are are multiple invalid value
                'four': ['contains invalid types of values ("1"). int or float required, str given.'],# returns expected value if there is an invalid types of value
                'five': ['contains invalid types of values ("1","2"). int or float required, str given.'],# returns expected value if there are multiple invalid types of value
                'six': ['4,"2" are invalid values.', 'contains invalid types of values ("2"). int or float required, str given.'],#returns expected value if there are  invalid value and  invalid types of values
                'seven':True
            },
        ]
    ]

    @data_provider(__data_for_test_are_valid_data___returns_expected_values)
    def test_are_valid_data__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        actual = pre_process_1.are_valid_data()
        self.assertDictEqual(expected, actual)

    __data_for_test_validate_one_hot_encoding___returns_expected_values = lambda: [
        [
            pd.DataFrame({}),
            {
                'one': {
                    'one_hot_encoding': True,
                    'available_values':[1,2]
                },
                'two': {
                    'one_hot_encoding': True,
                    'conversion':{'_NaN':94},
                    'available_values': [1, 2]
                },
                'three': {
                },
            },
            ['one_1','one_2','two_1','two_2','two_94']
        ]
    ]

    @data_provider(__data_for_test_validate_one_hot_encoding___returns_expected_values)
    def test_validate_one_hot_encoding__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.validate_one_hot_encoding()
        self.assertListEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()

