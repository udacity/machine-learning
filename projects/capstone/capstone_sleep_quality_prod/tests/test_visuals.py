import unittest
import sys,os
import pandas as pd
import numpy as np
sys.path.append(os.pardir)
from visuals import Visuals
from assert_method_is_called import assertMethodIsCalled
from pandas.util.testing import assert_frame_equal
from unittest_data_provider import data_provider
from collections import OrderedDict

class TestVisuals(unittest.TestCase):
    def setUp(self):
        self.ins = Visuals()

    __data_for_test_apply_range_classification__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([0, 99.9, 100, 199.9, 200, 299.9, 300], index=[0, 1, 2, 3, 4, 5, 6]),
                }
            ),
            3,
            0,
            300,
            None,
            OrderedDict([
                ('0-100', 2), ('100-200', 2), ('200-300', 2),
            ])
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([0, 99.9, 100, 199.9, 200, 299.9, 300], index=[0, 1, 2, 3, 4, 5, 6]),
                }
            ),
            3,
            0,
            300,
            'ordered_dict',
            OrderedDict([
                ('0-100', 2), ('100-200', 2), ('200-300', 2),
            ])
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([0, 99.9, 100, 199.9, 200, 299.9, 300], index=[0, 1, 2, 3, 4, 5, 6]),
                }
            ),
            3,
            0,
            300,
            'tuples',
            ('0-100', '100-200', '200-300'),
            (2, 2, 2)
        ],
    ]

    @data_provider(__data_for_test_apply_range_classification__returns_expected_values)
    def test_apply_range_classification__returns_expected_values(self, df, num_of_classes, r_min, r_max, return_type, expected_1,expected_2=None):
        if return_type == None:
            actual = self.ins.apply_range_classification(df['one'], num_of_classes, r_min, r_max)
            self.assertEqual(expected_1, actual)
        elif return_type == 'ordered_dict':
            actual = self.ins.apply_range_classification(df['one'], num_of_classes, r_min, r_max, return_type)
            self.assertEqual(expected_1, actual)
        elif return_type == 'tuples':
            actual_1, actual_2 = self.ins.apply_range_classification(df['one'], num_of_classes, r_min, r_max, return_type)
            self.assertTupleEqual(expected_1, actual_1)
            self.assertTupleEqual(expected_2, actual_2)

    __data_for_test_apply_simple_classification__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([0, 1, 2, 0, 1, 2, 0, 1, 2], index=[0, 1, 2, 3, 4, 5, 6, 7, 8]),
                }
            ),
            0,
            2,
            'ordered_dict',
            OrderedDict([
                (0, 3), (1, 3), (2, 3),
            ])
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([0, 1, 2, 0, 1, 2, 0, 1, 2], index=[0, 1, 2, 3, 4, 5, 6, 7, 8]),
                }
            ),
            1,
            2,
            'ordered_dict',
            OrderedDict([
                (1, 3), (2, 3),
            ])
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([0, 1, 2, 0, 1, 2, 0, 1, 2], index=[0, 1, 2, 3, 4, 5, 6, 7, 8]),
                }
            ),
            0,
            2,
            'tuples',
            (0, 1, 2),
            (3, 3, 3),
        ]
    ]

    @data_provider(__data_for_test_apply_simple_classification__returns_expected_values)
    def test_apply_simple_classification__returns_expected_values(self, df, r_min, r_max, return_type,
                                                                 expected_1, expected_2=None):
        if return_type == None:
            actual = self.ins.apply_simple_classification(df['one'], r_min, r_max)
            self.assertEqual(expected_1, actual)
        elif return_type == 'ordered_dict':
            actual = self.ins.apply_simple_classification(df['one'], r_min, r_max, return_type)
            self.assertEqual(expected_1, actual)
        elif return_type == 'tuples':
            actual_1, actual_2 = self.ins.apply_simple_classification(df['one'],  r_min, r_max,return_type)
            self.assertTupleEqual(expected_1, actual_1)
            self.assertTupleEqual(expected_2, actual_2)

    __data_for_test_classificate__returns_expected_values = lambda: [
        [
            pd.DataFrame(
                {
                    'one': pd.Series([100, 200, 300, 100, 200, 300, 100, 200, 300], index=[0, 1, 2, 3, 4, 5, 6, 7, 8]),
                }
            ),
            3,
            0,
            300,
            None,
            OrderedDict([
                ('0-100', 3), ('101-200', 3), ('201-300', 3),
            ])
        ],
        [
            pd.DataFrame(
                {
                    'one': pd.Series([0, 1, 2, 0, 1, 2, 0, 1, 2], index=[0, 1, 2, 3, 4, 5, 6, 7, 8]),
                }
            ),
            3,
            0,
            2,
            None,
            OrderedDict([
                (0, 3), (1, 3), (2, 3),
            ])
        ],
    ]

    @data_provider(__data_for_test_classificate__returns_expected_values)
    def test_classificate__returns_expected_values(self, df, num_of_classes, r_min, r_max, return_type, expected_1,
                                                   expected_2=None):
        if num_of_classes == r_max + 1:
            with assertMethodIsCalled(self.ins, "apply_simple_classification"):
                self.ins.classificate(df['one'], num_of_classes, r_min, r_max)
        else:
            with assertMethodIsCalled(self.ins, "apply_range_classification"):
                self.ins.classificate(df['one'], num_of_classes, r_min, r_max)



if __name__ == "__main__":
    unittest.main()