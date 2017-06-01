#
#  Tachyon
#  lexer_tester.py
#
#  Created on 30/05/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))
import src.lexer


class LexerTestCase(unittest.TestCase):
    """ Tests for lexer.py """

    # Create object of lexer to test on
    lexerTestObject = src.lexer.Lexer()


    def test_get_matcher_method_with_two_item(self):
        """ Testing getMatcher() method

        This will check that the return statement from this method is the correct joined
        list and correct amount of indexes to skip based on how many items were given and
        looped through to find matcher and complete the string.
        
        Input:
            matcher (string)    : "
            current_index (int) : 0
            source_code (list)  : ['"Ryan', 'Maugin"']

        Expected Output:
            return (list)       : ['"Ryan Maugin"', 1]
        """

        # This will run the assertEqual to see if input is equal to our wanted output
        self.assertEqual( 
            self.lexerTestObject.getMatcher('"', 0, ['"Ryan', 'Maugin"']),
            ['"Ryan Maugin"', 1]
        )

        # This will print out if the test was successful in logs when running test
        print("SUCCESSFUL - Test getMatcher() method with two items")



if __name__ == '__main__':
    unittest.main()