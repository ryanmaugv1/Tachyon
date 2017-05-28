#
#  Tachus
#  lexer.py
#
#  Created on 26/05/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import re # for performing regex expressions

class Lexer(object):

    # Reserved keywords for programming language
    KEYWORDS = ["function", "class", "if", "true", "false", "nil"]
    DATATYPE = ["bool", "int", "str"]


    def tokenize(self, source_code):

        # This will hold a record of all the tokens
        tokens = []

        # Cleanup code by removing extra line breaks
        source_code = source_code.split()

        # Current character position we are parsing
        source_index = 0

        # Will loop through each word in 
        while source_index < len(source_code) - 1:
            
            # This will be the word that is retrieved from source code
            word = source_code[source_index]

            # Check for new lines and ignore them
            if word in "\n": pass

            # Identify all of the Data Types
            elif word in self.DATATYPE:
                tokens.append("[DATATYPE " + word + "]")
            
            # Identify all the indentifiers which are all in 'KEYWWORDS' const
            elif word in self.KEYWORDS:
                tokens.append("[IDENTIFIER " + word + "]")

            # Identify all aithmetic operations in source code
            elif word in "*-/+%":
                tokens.append("[OPERATOR " + word + "]")

            # Identify all integer (number) values
            elif re.match(".[0-9]", word):
                tokens.append("[INTEGER " + word + "]")

            # Identifiy integer with a ';' at the end which terminates a statement and creates a token for the statement ender and number
            elif re.match(".[0-9$;]", word):
                tokens.append("[INTEGER " + word[:-1] + "]") 
            
            # Checks for the end of a statement ';'
            if ";" in word:
                tokens.append("[STATEMENT_END ;]")
            
            # Increment to the next word in tachus source code
            source_index += 1

        print(tokens)