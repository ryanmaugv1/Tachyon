#
#  Tachyon
#  parser.py
#
#  Created on 03/06/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

class Parser(object):

    def parse(self, token_stream):
        """ Parse

        This will parse the tokens given as argument and turn the sequence of tokens into 
        abstract syntax trees

        Args:
         token_stream (list) : The tokens produced by lexer
        """
        print(token_stream)


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
        """ Parsing Variable decleration

        This will parse through a variable decleration and create it's abstract tree and handle any
        syntax errors

        Args:
            token_stream (list) : List of tokens starting from where if statement was found

        Returns:
            AST : The variable decleration abstract syntax tree
        """
        print("PRINT")