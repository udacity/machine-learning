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

#https://pypi.python.org/pypi/unittest-data-provider/1.0.0
def data_provider(fn_data_provider):
    """Data provider decorator, allows another callable to provide the data for the test"""
    def test_decorator(fn):
        def repl(self, *args):
            for i in fn_data_provider():

                try:
                    fn(self, *i)
                except AssertionError:
                    print "Assertion error caught with data set ", i
                    raise
        return repl
    return test_decorator

class TestPreProcess(unittest.TestCase):
    __test_data = lambda:[
        [
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 98,  np.NaN, 94 ], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 98,  np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            ),
            OrderedDict([
                ('one',{98: '_mean', 99: '_mean', '_NaN': 'mean', 94: 'something'} ),
                ('two',{})
            ]),
            pd.DataFrame(
                {
                    'one': pd.Series([1, 2, 1.5, 'mean','something'], index=[0, 1, 2, 3, 4]),
                    'two': pd.Series([1, 2, 98, np.NaN, 94], index=[0, 1, 2, 3, 4])
                }
            )
        ]
    ]

    __test_data_2 = lambda:[
        [
            pd.DataFrame({
                'one': pd.Series([1, 2],index=[0, 1])
            }),
            1.5
        ]
    ]

    @data_provider(__test_data)
    def test_convert_values_and_extract_data(self,data,columns_info,expected):
        actual =  pre_process.convert_values_and_extract_data(data, columns_info)
        assert_frame_equal(actual,expected)

    @data_provider(__test_data_2)
    def test_average(self,nums,expected):
        actual =  pre_process.average(nums['one'])
        self.assertEqual(expected,actual)




if __name__ == "__main__":
    unittest.main()

