#
#  Tachyon
#  parser.py
#
#  Created on 03/06/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import constants # for constants like tachyon keywords and dataypes

class Parser(object):

    def parse(self, token_stream):
        """ Parsing

        This will parse the tokens given as argument and turn the sequence of tokens into 
        abstract syntax trees

        Args:
         token_stream (list) : The tokens produced by lexer
        """

        # Complete Abstract Syntax tree
        source_ast = []
        
        # This will hold the token index we are parsing at
        token_index = 0

        # Loop through each token
        while token_index < len(token_stream):
            
            print(token_stream[token_index])

            # Increment token index by 1 when a loop finishes
            token_index += 1


    def parse_if_statement(self, token_stream):
        """ Parsing If Statement
        
        This will parse through an if statement and create it's abstract tree and handle any
        syntax error

        Args:
            token_stream (list) : List of tokens starting from where if statement was found

        Returns:
            AST : The if statement abstract syntax tree
        """
        print("IF STATEMENT")


    def parse_variable_decleration(self, token_stream):
        """ Parsing Variable decleration

        This will parse through a variable decleration and create it's abstract tree and handle any
        syntax errors

        Args:
            token_stream (list) : List of tokens starting from where if statement was found

        Returns:
            AST : The variable decleration abstract syntax tree
        """
        print("VARIABLE DECLERATION")

    
    def parse_print(self, token_stream):
        """ Parsing print

        This will parse through a variable decleration and create it's abstract tree and handle any
        syntax errors

        Args:
            token_stream (list) : List of tokens starting from where if statement was found

        Returns:
            AST : The variable decleration abstract syntax tree
        """
        print("PRINT")