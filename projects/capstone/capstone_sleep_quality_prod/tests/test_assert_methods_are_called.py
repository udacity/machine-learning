import unittest
import sys,os
import pandas as pd
import numpy as np
sys.path.append(os.pardir)

from assert_methods_are_called import assertMethodsAreCalled
from pandas.util.testing import assert_frame_equal
from unittest_data_provider import data_provider
from collections import OrderedDict

class TestVisuals(unittest.TestCase):

    __data_for_test_assert_methods_are_called__returns_expected_values = lambda: [
        [
            {'MockClass1':'b'},
        ],
        [
            {'MockClass1': ['b','c']},
        ],
        [
            {'MockClass1': ['b', 'c'],'MockClass2': ['b', 'c']},
        ],
    ]

    @data_provider(__data_for_test_assert_methods_are_called__returns_expected_values)
    def test_assert_methods_are_called__returns_expected_values(self, objs_and_methods,expected_2=None):
        with assertMethodsAreCalled(self.ins, "apply_simple_classification"):
            self.ins.assert_methods_are_called()
        # if num_of_classes == r_max + 1:
        #     with assertMethoCalled(self.ins, "apply_simple_classification"):
        #         self.ins.assert_methods_are_called(df['one'], num_of_classes, r_min, r_max)
        # else:
        #     with assertMethodIsCalled(self.ins, "apply_range_classification"):
        #         self.ins.assert_methods_are_called(df['one'], num_of_classes, r_min, r_max)

class MockClass1:
    def a(self):
        self.b()
        self.c()
        return
    def b(self):
        return
    def c(self):
        return

class MockClass2:
    def a(self):
        self.b()
        self.c()
        return
    def b(self):
        return
    def c(self):
        return

if __name__ == "__main__":
    unittest.main()