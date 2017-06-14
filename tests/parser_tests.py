#
#  Tachyon
#  parser_tester.py
#
#  Created on 11/06/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))
import src.parser


class ParserTestCase(unittest.TestCase):
    """ Tests for parser methods """

    # Create parser instance to test on
    parserObject = src.parser.Parser([['DATATYPE', 'int'], ['IDENTIFIER', 'a'], ['OPERATOR', '='], ['INTEGER', '11'], ['STATEMENT_END', ';'], 
                                      ['DATATYPE', 'str'], ['IDENTIFIER', 'name'], ['OPERATOR', '='], ['STRING', '"Ryan Maugin The Boss"'], ['STATEMENT_END', ';']])

    
    # 
    #
    #  TESTS for does_var_exist(self, name) method
    #
    #

    def test_does_var_exist_with_valid_case(self):

        # Check that inputting a variable name to see if it exists or not
        self.assertEqual(self.parserObject.does_var_exist('test'), True)
        print('SUCCESS')


if __name__ == '__main__':
    unittest.main()