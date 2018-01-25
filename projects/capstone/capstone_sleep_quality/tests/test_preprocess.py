import pandas as pd
import numpy as np
import sys,os
sys.path.append(os.pardir)
import sample
import pre_process
from pandas.util.testing import assert_frame_equal,assert_series_equal
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
                    'two': pd.Series([1.1,2.1,3.1,4.1,5.1], index=[0, 1, 2, 3, 4]),
                    'three': pd.Series([1, 2, 98,  np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'four': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'five': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            ),
            {
                'one':{
                    'conversion': {
                        'values':{
                            98: '_mean',  # if "_mean" is specified to convert to give a average of  the column
                            '_NaN': 'mean',  # if '_NaN' is specified to convert from NaNs are converted to converted to
                            94: 'something'  # convert convert_from to convert to
                        }
                    }
                },
                'two':{
                    'conversion': {
                        'astype': 'int32'
                    }
                },
                'three': {

                },
                'four': {
                    'conversion': {
                        'values':{}
                    }
                },
                'five': {
                    'conversion': {
                        'astype': False
                    }
                },
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 1.5, 'mean','something'], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 3, 4, 5], index=[0, 1, 2, 3, 4]),
                    'three': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'four': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'five': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4])
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

    # python test_preprocess.py TestPreProcess.test_recalculation__return_expected_values
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
                        'values':{
                            '_NaN': 94
                        }

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


    # python test_preprocess.py TestPreProcess.test_validate_one_hot_encoding__returns_expected_values
    __data_for_test_validate_one_hot_encoding___returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2,2], index=[0, 1, 2]),
                    'two': pd.Series([1, 2,float('NaN')], index=[0, 1, 2]),
                    # 'three': pd.Series([1, 4, 5], index=[0, 1, 2]),
                }
            ),
            {
                'one': {
                    'one_hot_encoding': True,
                    'available_values':[1,2]
                },
                'two': {
                    'one_hot_encoding': True,
                    'conversion':{
                        'values':{
                            '_NaN': 94
                        },
                        'astype': 'int64'
                    },
                    'available_values': [1, 2]
                },
            },
            # ['one_1','one_2','two_1','two_2','two_94'],
            [],
            []
        ]
    ]

    @data_provider(__data_for_test_validate_one_hot_encoding___returns_expected_values)
    def test_validate_one_hot_encoding__returns_expected_values(self, df, columns_config,expected_1,expected_2 ):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.convert_values_and_extract_data()
        pre_process_1.apply_one_hot_encoding()
        actual_1,actual_2 = pre_process_1.validate_one_hot_encoding()
        self.assertListEqual(expected_1, actual_1)
        self.assertListEqual(expected_2, actual_2)





    # # python test_preprocess.py TestPreProcess.test_set_target_column_names__returns_expected_values
    # __data_for_test_set_target_column_names___returns_expected_values = lambda: [
    #     [
    #         pd.DataFrame(
    #             {
    #                 'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
    #             }
    #         ),
    #         {
    #             'three': {
    #                 'is_target_variable': True
    #
    #             },
    #         },
    #         ['three']
    #     ],
    #     [
    #         pd.DataFrame(
    #             {
    #                 'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
    #             }
    #         ),
    #         {
    #             'three': {
    #                 'is_target_variable': False
    #             },
    #         },
    #         []
    #     ],
    #     [
    #         pd.DataFrame(
    #             {
    #                 'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
    #             }
    #         ),
    #         {
    #             'three': {
    #             },
    #         },
    #         []
    #     ]
    # ]
    #
    # @data_provider(__data_for_test_set_target_column_names___returns_expected_values)
    # def test_set_target_column_names__returns_expected_values(self, df, columns_config, expected):
    #     pre_process_1 = pre_process.PreProcess(df, columns_config)
    #     pre_process_1.set_target_column_names()
    #     actual = pre_process_1.target_column_names
    #     self.assertListEqual(expected, actual)
    #
    # python test_preprocess.py TestPreProcess.test_get_inputs_and_outputs__returns_expected_values
    # __data_for_test_c___returns_expected_values = lambda: [
    #     [
    #         pd.DataFrame(
    #             {
    #                 'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
    #                 'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
    #                 'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
    #             }
    #         ),
    #         {
    #             'one': {
    #             },
    #             'two': {
    #             },
    #             'three': {
    #                 'is_target_variable': True
    #
    #             },
    #         },
    #         pd.DataFrame(
    #             {
    #                 'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
    #                 'two': pd.Series([1, 2, 3], index=[0, 1, 2])
    #             }
    #         ),
    #         pd.DataFrame(
    #             {
    #                 'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
    #             }
    #         )
    #
    #     ]
    # ]
    # @data_provider(__data_for_test_get_inputs_and_outputs___returns_expected_values)
    # def test_get_inputs_and_outputs__returns_expected_values(self, df, columns_config, expected_1, expected_2):
    #     pre_process_1 = pre_process.PreProcess(df, columns_config)
    #     actual_1, actual_2 = pre_process_1.get_inputs_and_outputs()
    #     assert_frame_equal(expected_1, actual_1, check_dtype=False, check_like=True)
    #     assert_frame_equal(expected_2, actual_2, check_dtype=False, check_like=True)
    # python test_preprocess.py TestPreProcess.test_drop_columns_by_regexp__returns_expected_values
    __data_for_test_drop_columns_by_regexp__returns_expected_values = lambda: [
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
                    'one_hot_encoding': True,
                    'available_values': [1, 2]
                },
                'two': {
                    'one_hot_encoding': True,
                    'conversion': {
                        'values': {
                            '_NaN': 94
                        },
                        'astype': 'int64'
                    },
                    'available_values': [1, 2]
                },
            },
            ['94$','96$'],
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
                }
            ),

        ]
    ]
    @data_provider(__data_for_test_drop_columns_by_regexp__returns_expected_values)
    def test_drop_columns_by_regexp__returns_expected_values(self, df, patterns, expected):
        pre_process_1 = pre_process.PreProcess(df, patterns)
        pre_process_1.drop_columns_by_regexp(patterns)
        actual = pre_process_1.df
        assert_frame_equal(expected, actual, check_dtype=False, check_like=True)

    # python test_preprocess.py TestPreProcess.test_get_matched_column_names__returns_expected_values
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

    # python test_preprocess.py TestPreProcess.test_get_column_names_to_apply_log_trans__returns_expected_values
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


    # python test_preprocess.py TestPreProcess.test_apply_log_trans_according_to_columns_config__returns_expected_values
    __data_for_test_apply_log_trans_according_to_columns_config__returns_expected_values = lambda: [
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

    @data_provider(__data_for_test_apply_log_trans_according_to_columns_config__returns_expected_values)
    def test_apply_log_trans_according_to_columns_config__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.apply_log_trans_according_to_columns_config()
        actual = pre_process_1.df
        assert_frame_equal(expected, actual)

    # python test_preprocess.py TestPreProcess.test_apply_log_trans_according_to_columns_config__returns_expected_values
    __data_for_test_apply_log_trans_according_to_columns_config__returns_expected_values = lambda: [
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

    @data_provider(__data_for_test_apply_log_trans_according_to_columns_config__returns_expected_values)
    def test_apply_log_trans_according_to_columns_config__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.apply_log_trans_according_to_columns_config()
        actual = pre_process_1.df
        assert_frame_equal(expected, actual)

    # python test_preprocess.py TestPreProcess.test_apply_log_trans__returns_expected_values
    __data_for_test_apply_log_trans__returns_expected_values = lambda: [
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

    @data_provider(__data_for_test_apply_log_trans__returns_expected_values)
    def test_apply_log_trans__returns_expected_values(self, df, columns_config, columns_to_apply, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.apply_log_trans(columns_to_apply)
        actual = pre_process_1.df
        assert_frame_equal(expected, actual)



    # python test_preprocess.py TestPreProcess.test_convert_values__return_expected_values
    __data_for_test_convert_values__return_expected_values = lambda:[
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 98,  np.NaN, 94 ], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'three': pd.Series([1, 2, 98,  np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            ),
            {
                'one':{
                    'conversion': {
                        'values':{
                            98: '_mean',  # if "_mean" is specified to convert to give a average of  the column
                            '_NaN': 'mean',  # if '_NaN' is specified to convert from NaNs are converted to converted to
                            94: 'something'  # convert convert_from to convert to
                        }
                    }
                },
                'two':{

                },
                'three': {
                    'conversion': {
                        'values': {}
                    }
                }
            },
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 1.5, 'mean','something'], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4]),
                    'three': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            )
        ]
    ]

    @data_provider(__data_for_test_convert_values__return_expected_values)
    def test_convert_values__return_expected_values(self, data, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(data, columns_config)
        pre_process_1.convert_values()
        actual = getattr(pre_process_1, "df")
        assert_frame_equal(expected, actual, check_dtype = False, check_like = True)

    # @data_provider(__data_for_test_apply_log_trans__returns_expected_values)
    # def test_apply_log_trans__returns_expected_values(self, df, columns_config, expected):
    #     pre_process_1 = pre_process.PreProcess(df, columns_config)
    #     pre_process_1.apply_log_trans()
    #     actual = pre_process_1.df
    #     assert_frame_equal(expected, actual)



    # python test_preprocess.py TestPreProcess.test_convert_types__return_expected_values
    __data_for_test_convert_types__return_expected_values = lambda: [
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
                        'astype': 'int32'
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

    @data_provider(__data_for_test_convert_types__return_expected_values)
    def test_convert_types__return_expected_values(self, data, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(data, columns_config)
        pre_process_1.convert_types()
        actual = getattr(pre_process_1, "df")
        assert_frame_equal(expected, actual, check_dtype=False, check_like=True)

# python test_preprocess.py TestPreProcess.test_convert_types__return_expected_values
    __data_for_test_convert_types__return_expected_values = lambda: [
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
                        'astype': 'int32'
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

    @data_provider(__data_for_test_convert_types__return_expected_values)
    def test_convert_types__return_expected_values(self, data, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(data, columns_config)
        pre_process_1.convert_types()
        actual = getattr(pre_process_1, "df")
        assert_frame_equal(expected, actual, check_dtype=False, check_like=True)

    # python test_preprocess.py TestPreProcess.test_get_column_names_contain_continuous_values__returns_expected_values
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

    # python test_preprocess.py TestPreProcess.test_get_skews__returns_expected_values
    __data_for_test_get_skews__returns_expected_values = lambda: [
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
            [0.0, 0.0]
            # pd.DataFrame(
            #     {
            #         'one': pd.Series([1, 2, 3], index=[0, 1, 2]),
            #         'two': pd.Series([1, 2, 3], index=[0, 1, 2]),
            #         'three': pd.Series([1, 2, 3], index=[0, 1, 2]),
            #         'four': pd.Series([1, 2, 3], index=[0, 1, 2]),
            #     }
            # ),
        ]
    ]

    @data_provider(__data_for_test_get_skews__returns_expected_values)
    def test_get_skews__returns_expected_values(self, df, columns_config, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        actual = pre_process_1.get_skews()
        self.assertItemsEqual(expected, actual)



    # python test_preprocess.py TestPreProcess.test_get_skews__returns_expected_values
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


    # python test_preprocess.py TestPreProcess.test_check_if_columns_contain_negative_values__returns_expected_values
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

    # python test_preprocess.py TestPreProcess.test_raise_values_to_positive__returns_expected_values
    __data_for_test_raise_values_to_positive__returns_expected_values = lambda: [
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

    @data_provider(__data_for_test_raise_values_to_positive__returns_expected_values)
    def test_raise_values_to_positive__returns_expected_values(self, df, columns_config,min, expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.raise_values_to_positive(min)
        actual = pre_process_1.df
        assert_frame_equal(expected, actual)


    # python test_preprocess.py TestPreProcess.test_set_log_trans_based_on_skewness__returns_expected_values
    __data_for_test_set_log_trans_based_on_skewness__returns_expected_values = lambda: [
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
                    'continuous': True
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

    @data_provider(__data_for_test_set_log_trans_based_on_skewness__returns_expected_values)
    def test_set_log_trans_based_on_skewness__returns_expected_values(self, df, columns_config, allowed_skew,  expected):
        pre_process_1 = pre_process.PreProcess(df, columns_config)
        pre_process_1.set_log_trans_based_on_skewness(allowed_skew)
        actual = pre_process_1.columns_config
        self.assertDictEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()

