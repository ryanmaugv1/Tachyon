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
import objgen

def main():
    
    # This variable will hold the contents of the source code
    content = ""
    # Open source code file and get it's content
    with open(os.path.dirname(os.path.realpath(__file__)) + "/test.txt", "r") as file:
        # Append the contents of the file to the content variable
        content = file.read()
    
    # --------------------------------------
    #  LEXER
    # --------------------------------------

    # Create an instance of the lexer class
    lex = lexer.Lexer()
    # Call lexer method to perform lexical analysis on code
    tokens = lex.tokenize(content)

    # --------------------------------------
    #  PARSER
    # --------------------------------------

    # Create an instance of the parser class
    Parser = parser.Parser(tokens)

    # Call the parser method and pass in the tokens as arguments
    source_ast = Parser.parse(tokens)

    # --------------------------------------
    # Object Generation
    # --------------------------------------

    # Create an instance of the Object Generator (objgen) class
    object_generator = objgen.ObjectGenerator(source_ast)

    # Call the object definer to get python exec() string
    exec_string = object_generator.object_definer()

main()

