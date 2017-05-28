#
#  Tachus
#  main.py
#
#  Created on 27/05/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import os
import lexer

##
#  Will call lexical analysis method from lexer class and
#  give in source code content to it in oerder to get tokens
##
def lexical_analyzer():
    # Create an instance of the lexer class
    lex = lexer.Lexer()
    content = ""

    # Open source code file and get it's content
    with open(os.path.dirname(os.path.realpath(__file__)) + "/test.txt", "r") as file:
        content = file.read()
    
    # Call lexer method to perform lexical analysis on code
    tokens = lex.tokenize(content)

lexical_analyzer()

