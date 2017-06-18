#
#  Tachyon
#  parser.py
#
#  Created on 03/06/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

from ast import literal_eval # To perform ast literal eval to figure out a strings data type
import constants # for constants like tachyon keywords and datatypes

class Parser(object):


    
    def __init__(self, token_stream):
        # Complete Abstract Syntax tree
        self.source_ast = { 'main_scope': [] }
        # Symbol table fo variable semantical analysis
        self.symbol_tree = []
        # This will hold all the tokens
        self.token_stream = token_stream
        # This will hold the token index we are parsing at
        self.token_index = 0


    
    def parse(self, token_stream):
        """ Parsing

        This will parse the tokens given as argument and turn the sequence of tokens into 
        abstract syntax trees

        Args:
         token_stream (list) : The tokens produced by lexer
        """
        print('---------------------------------------------')
        print(token_stream)
        print('---------------------------------------------')
        print("//////////////// DEBUG ZONE ////////////////")

        # Loop through each token
        while self.token_index < len(token_stream):

            # Set the token values in variables for clearer and easier debugging and readability
            token_type = token_stream[self.token_index][0]
            token_value = token_stream[self.token_index][1]

            # This will check for an if statement token
            if token_type == 'IDENTIFIER' and token_value.lower() == 'if':
                print('-----')


            # This will parse for a vraible decleration token
            if token_type == 'DATATYPE' and token_value.lower() in constants.DATATYPE:
                print(token_value)