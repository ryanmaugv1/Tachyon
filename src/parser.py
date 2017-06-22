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

        # Loop through each token
        while self.token_index < len(token_stream):

            # Set the token values in variables for clearer and easier debugging and readability
            token_type = token_stream[self.token_index][0]
            token_value = token_stream[self.token_index][1]

            # This will check for an if statement token
            if token_type == 'IDENTIFIER' and token_value.lower() == 'if':
                self.parse_if_statement(self.token_index, token_stream[self.token_index:len(token_stream)])

            # This will parse for a vraible decleration token
            if token_type == 'DATATYPE' and token_value.lower() in constants.DATATYPE:
                self.token_index += self.parse_variable_decleration(self.token_index, token_stream[self.token_index:len(token_stream)])
                continue

            # Increment index of source code token being checked
            self.token_index += 1
        
        print(self.source_ast)
        print('############################')
        print(self.token_stream)
        

        
    def parse_variable_decleration(self, token_index, token_stream):
        """ Parsing Variable Decleration

        This will parse variable decleration token stream that matcher variable
        decleration pattern.

        Args:
            token_index (int)   : This will hold the index where the decleration pattern starts 
            token_stream (list) : The token_stream from token index to end of source code tokens
        Returns:
            tokens_checked (int) : The amounts of token from the index that have been checked 
        """
        
        # The Variable Decleration AST
        ast = { 'VariableDecleration': [] }
        # Marks if the terminator ';' is found
        found_terminator = False
        # Hold the number of tokens checked
        tokens_checked = 0

        # Loop through the source code and form the parse tree for the var decleration
        for x in range(0, len(token_stream)):
            tokens_checked += 1

            # Check if the end statement is found and exit loop and form parse tree
            if token_stream[x][1] == ';': 
                found_terminator = True   
                break

            # This will check the variable data type and add it to the ast
            if token_stream[x][0] == 'DATATYPE': 
                ast['VariableDecleration'].append({ 'type': token_stream[x][1] })

            # Check variable name and add it to symbol tree if it doesn't already exist
            if token_stream[x][0] == 'IDENTIFIER' and x == 1: 
                if self.does_var_exist(token_stream[x][1]) == False:
                    ast['VariableDecleration'].append({ 'name': token_stream[x][1] })

            if token_stream[x][1] != '=' and x == 2:
                self.error_message(token_index + tokens_checked, "SyntaxError: An equal sign '=' was excpexted in variable decleration")
            
            # Get the value of the variable decleration
            if x >= 3:
                if str(type(literal_eval(token_stream[x][1]))) == "<class " + "'" + ast['VariableDecleration'][0]['type'] + "'>":
                    ast['VariableDecleration'].append({ 'value': token_stream[x][1] })
                    #TODO ADD ERROR HANDLING FOR IF VARIABLE VALUE IS NOT SAME TYPE AS DATATYPE STATED
                else:
                    self.error_message(token_index + tokens_checked, "TypeError: Variable value does not conform to type of " + ast['VariableDecleration'][0]['type'])

        # If the end statement was never found then throw an error
        if found_terminator == False: self.error_message(token_index, 'SyntaxError: Variable Decleration did not end with ";"')

        # Add variable decleration ast to full source code ast
        self.source_ast['main_scope'].append(ast)
        # Remove the tokens that have been checked by parser
        self.remove_checked_tokens(token_index, tokens_checked)
        # Return the number of tokens thta have been checked
        return tokens_checked

        

    def parse_if_statement(self, token_index, token_stream):
        print('IF STATEMENT')



    def error_message(self, token_index, error_message):
        print("[Index: {}] {}".format(token_index, error_message))
        quit()


    
    def does_var_exist(self, var_name):
        # This loops through the symbol tree and check every variable name to see if there are any that match
        for item in self.symbol_tree:
            if item[0] == var_name: 
                self.error_message(self.token_index, 'SemanticError: Variable "' + var_name + '" already exists!')
        return False



    def remove_checked_tokens(self, start_index, tokens_checked):
        for x in range(start_index, start_index + tokens_checked):
            print(self.token_stream[x])
            self.token_stream[x] = ''
        print('--------')