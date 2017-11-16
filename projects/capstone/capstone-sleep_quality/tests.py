import unittest
import sys
import sample
# def data_provider(fn_data_provider):
#     """Data provider decorator, allows another callable to provide the data for the test"""
#     def test_decorator(fn):
#         def repl(self, *args):
#             for i in fn_data_provider():
#                 try:
#                     fn(self, *i)
#                 except AssertionError:
#                     print "Assertion error caught with data set ", i
#                     raise
#         return repl
#     return test_decorator



class TestSample(unittest.TestCase):
    def test_add(self):
        print 'ok'
        self.assertEqual(sample.add(1, 2), 3)

if __name__ == "__main__":
    unittest.main()