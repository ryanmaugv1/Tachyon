#
#  Tachyon
#  syntatic_parsing.py
#
#  Created on 03/06/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import constants # for constants like tachyon keywords and datatypes

class SyntaxParser(object):


    
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

        # Loop through each token
        while self.token_index < len(token_stream):

            # Set the token values in variables for clearer and easier debugging and readability
            token_type = token_stream[self.token_index][0]
            token_value = token_stream[self.token_index][1]
            
            if token_type == "DATATYPE":
                self.variable_decleration_parsing(token_stream[self.token_index:len(token_stream)])

            self.token_index += 1


    
    def variable_decleration_parsing(self, token_stream):
        """ Variable Decleration Parsing

        This method will parse variable declerations and add themto the source AST

        Args:
            token_stream (list) : The token stream starting from where var decleration was found
        """

        ast = { 'VariableDecleration': [] }  # The abstract syntax tree for var decl
        tokens_checked = 0                   # Number of token checked that made up the var decl

        for x in range(0, len(token_stream)):
            
            # Create variables for identifying token type and value more easily
            token_type = token_stream[x][0]
            token_value = token_stream[x][1]

            # Skip the '=' operator in var decl
            if x == 2 and token_type == "OPERATOR" and token_value == "=":
                pass

            # If a statement end is found then break out parsing
            if token_stream[x][0] == "STATEMENT_END": break
            
            # This will parse the first token which will be the var type
            if x == 0: ast['VariableDecleration'].append({ "type": token_value })

            # This will pase the second token which will be the name of the var
            if x == 1 and token_type == "IDENTIFIER": ast['VariableDecleration'].append({ "name": token_value })

            # This will parse the 3rd token which adds the value of the variable
            if x == 3 and token_stream[x + 1][0] == "STATEMENT_END":
                #TODO If identifier as value then search through symbol tree method
                # Add value as a number not a string if it is an int or else add it as a string
                try: ast['VariableDecleration'].append({ "value": int(token_value) })
                except ValueError: ast['VariableDecleration'].append({ "value": token_value })
            
            # TODO Handle concat and arithmetics to declare a variable
            # This will parse any variable declerations which have concatenation or arithmetics
            # elif x >= 3:
            #     for valItem in range(tokens_checked, len(token_stream)):
            #         if token_stream[valItem][0] == "STATEMENT_END": break

            #         # do something

            #         tokens_checked += 1
            #     break

            tokens_checked += 1
        
        print(ast)
        self.token_index += tokens_checked