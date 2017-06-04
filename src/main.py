#
#  Tachyon
#  main.py
#
#  Created on 27/05/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import os
import lexer
import parser


##
#  This will call the parser method inside of the parser class
#  passing in the tokens to perform semantic and syntatic analysis
##
def _parser(tokens):

    # Create an instance of the parser class
    Parser = parser.Parser()

    # Call the parser method and pass in the tokens as arguments
    Parser.parser(tokens) 



##
#  Will call lexical analysis method from lexer class and
#  give in source code content to it in order to return tokens
##
def lexical_analyzer():

    # Create an instance of the lexer class
    lex = lexer.Lexer()

    # This variable will hold the contents of the source code
    content = ""

    # Open source code file and get it's content
    with open(os.path.dirname(os.path.realpath(__file__)) + "/test.txt", "r") as file:

        # Append the contents of the file to the content variable
        content = file.read()
    
    # Call lexer method to perform lexical analysis on code
    tokens = lex.tokenize(content)

    # This will pass the generated tokens to the parser function
    _parser(tokens)


lexical_analyzer()

