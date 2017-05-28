#
#  Tachus
#  lexer.py
#
#  Created on 26/05/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import os

class Lexer(object):

    # Reserved keywords for programming language
    KEYWORDS = ["function", "class", "if", "true", "false", "nil"]

    def tokenize(self, source_code):
        # Cleanup code by removing extra line breaks
        print(source_code)

