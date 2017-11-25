import unittest
from unittest_data_provider import data_provider
import sys,os
sys.path.append(os.pardir)
import str
# from .. import str
class TestPreProcess(unittest.TestCase):

    __data_for_test_convert_all_to_string__returns_expected_values = lambda: [
        [
            [1,1.5,'w'],False,['1','1.5','w']
        ],
        [
            [1, 1.5, 'w'], True, ['1', '1.5', '"w"']
        ],
    ]

    @data_provider(__data_for_test_convert_all_to_string__returns_expected_values)
    def test_convert_all_to_string__returns_expected_values(self, list_to_stringify, quote_string, expected):
        actual = str.convert_all_to_string(list_to_stringify,quote_string)
        self.assertEquals(expected, actual)

    __data_for_test_implode__returns_expected_values = lambda: [
        [
            [1, 1.5, 'w'],',',False, '1,1.5,w'
        ],
        [
            [1, 1.5, 'w'], ',', True, '1,1.5,"w"'
        ]
    ]

    @data_provider(__data_for_test_implode__returns_expected_values)
    def test_implode__returns_expected_values(self, list_to_stringify,separator,quote_string, expected):
        actual = str.implode(list_to_stringify,separator,quote_string)
        self.assertEquals(expected,actual)


if __name__ == "__main__":
    unittest.main()