#
#  Tachyon
#  main.py
#
#  Created on 27/05/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import os
import sys
import lexer
import parser
import objgen

def main():
    
    path     = os.getcwd() # Holds path this script was executed from
    fileName = sys.argv[1] # Holds the name of the file the user wants to compile
    content = ""           # This variable will hold the contents of the source code

    try:
        # Open source code file and get it's content and save it to the 'contents' var
        with open(path + "/" + fileName, "r") as file:
            content = file.read()
    except:
        print('Cannot find "' + fileName + '"')
    
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
    exec_string = object_generator.object_definer(False)

    # Execute the tachyon code that has been transpiled to python code to get output
    exec(exec_string)

main()

