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


    # 
    #
    #  TESTS for getMatcher() Method
    #
    #

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
            return (list)       : ['"Ryan Maugin"', '; ', 2]
        """

        # This will run the assertEqual to see if input is equal to our wanted output
        self.assertEqual( 
            self.lexerTestObject.getMatcher('"', 0, ['"Ryan', 'Maugin";']),
            ['"Ryan Maugin"', '; ', 1]
        )

        # This will print out if the test was successful in logs when running test
        print("SUCCESS - Testing getMatcher() method with two words")

    
    def test_get_matcher_method_with_sentence(self):

        # Check that a sentence has the correct input and iteration count with the correct end character
        self.assertEqual(
            self.lexerTestObject.getMatcher('"', 0, ['"Tachyon', 'programming', 'language', 'is', 'created by Ryan Maugin";']),
            ['"Tachyon programming language is created by Ryan Maugin"', '; ', 4]
        )

        # Print success message to logs if it doesn't fail
        print("SUCCESS - Testing if getMatcher() method can handle a sentence")


    def test_get_matcher_method_single_word_handling(self):

        # Check that the getMatcher() method can return correct string and end character if matchers ("")
        # are in the same source code item
        self.assertEqual(
            self.lexerTestObject.getMatcher('"', 0, ['"Hi";']),
            ['"Hi"', '', ';']
        )

        # Print success message if no errors occur
        print('SUCCESS - Testing if getMatcher() can handle single word')


    def test_get_matcher_method_without_extra_characters(self):

        # Check that the getMatcher() method returns empty string if there are no extra characters stuck to the
        # ending matcher (closing quote) of a string
        self.assertEqual(
            self.lexerTestObject.getMatcher('"', 0, ['"My', 'name', 'is', 'Ryan!"']),
            ['"My name is Ryan!"', ' ', 3]
        )

        # Print success message if no errors occur
        print("SUCCESS - Testing if getMatcher() can handle standalone string with no extra characters")

    
    def test_get_matcher_method_with_empty_string(self):

        # Check that if getMatcher() method get given an empty string "" will return an empty string
        self.assertEqual(
            self.lexerTestObject.getMatcher('"', 0, ['"";']),
            ['""', '', ';']
        )

        # Print success message if no errors occur
        print("SUCCESS - Testing if getMatcher() can handle empty strings")

    
    #
    #
    #  TESTS for Tokenize() Method
    #
    #

    def test_tokenize_method_with_variable_decleration(self):

        # Check that the tokenize() method can produce tokens for variable declaration source code
        self.assertEqual(
            self.lexerTestObject.tokenize('str name = "Ryan Maugin";'),
            ['[DATATYPE str]', '[IDENTIFIER name]', '[OPERATOR =]', '[STRING "Ryan Maugin"]', '[STATEMENT_END ;]']
        )

        # Print success message if it doesn't fail
        print("SUCCESS - Test that tokenize can return proper tokens for variable decleration code in tachyon")

    def test_tokenize_method_with_if_statement(self):

        # Check that the tokenize() method can produce tokens for a if statement source code
        self.assertEqual(
            self.lexerTestObject.tokenize('if name == "Ryan Maugin" { print name; }'),
            [
                '[IDENTIFIER if]', '[IDENTIFIER name]', '[COMPARISON_OPERATOR ==]', '[STRING "Ryan Maugin"]', '[SCOPE_DEFINER {]',
                '[IDENTIFIER print]', '[IDENTIFIER name;]', '[STATEMENT_END ;]', '[SCOPE_DEFINER }]'
            ]
        )

        # Print success message if it doesn't fail
        print('SUCCESS - Test that tokenize method can return proper tokens for if statment in tachyon')


if __name__ == '__main__':
    unittest.main()