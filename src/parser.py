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

        # This will hold the token index we are parsing at
        token_index = 0

        # Loop through each token
        while token_index < len(token_stream):

            # Set the token values in variables for clearer and easier debugging and readability
            token_type = token_stream[token_index][0]
            token_value = token_stream[token_index][1]

            # This will check for an if statement token
            if token_type == 'IDENTIFIER' and token_value.lower() == 'if':
                self.parse_if_statement(token_stream[token_index:len(token_stream)])

            # This will parse for a vraible decleration token
            if token_type == 'DATATYPE' and token_value.lower() in constants.DATATYPE:
                self.parse_variable_decleration(token_stream[token_index:len(token_stream)], token_index)

            # Increment token index by 1 when a loop finishes
            token_index += 1
        
        print("----------------------------------------------")
        print("ABSTRACT SYNTAX TREE: ", self.source_ast)
        print("SYMBOL TREE: ", self.symbol_tree)
        print("----------------------------------------------")



    def get_variable_value(self, name):
        """ Get the value of a variable

        This will get the value of a variable if it exists and return it

        Args:
            name (string) : The name of the variable we are searching for

        Returns:
            bool  : Will return False if the variable does not exist
            value : Will return the value of the 
        """
        for var in self.symbol_tree:
            if var[0] == name: return var[1]
        return False



    def parse_if_statement(self, token_stream):
        """ Parsing If Statement

        This will parse through an if statement and create it's abstract tree and handle any
        syntax error

        Args:
            token_stream (list) : List of tokens starting from where if statement was found

        Returns:
            AST : The if statement abstract syntax tree
        """
       
        # This will hold the AST for the if statement
        ast = { 'ConditionalStatement': [] }
        # This will hold the index when looping through if statement tokens
        index = 0

        for item in token_stream:
            
            # This will add one every loop to the index of the var decleration
            index += 1
            # Check for the beggining of the statement body
            if item[1] == '{': break

            # Check and create the ast for the if statement condition
            if index >= 2: 

                # This will check the identifiers in the 
                if item[0] == 'IDENTIFIER' and item[1] not in constants.KEYWORDS:

                    # This will call the get variable value and store the value inside the getting_var value
                    getting_var = self.get_variable_value(item[1]) 

                    # This will act accordingly depending on output
                    if getting_var != False:
                        ast['ConditionalStatement'].append({'value': item[1]})
                        print(getting_var)
                    else: print('Unexpected Identifier "' + item[1] + '" could not be found')
                
                # This will check for a comparison operator
                if item[0] == 'COMPARISON_OPERATOR':
                    #TODO Create an add to the syntax tree
                    ast['ConditionalStatement'].append({'comparison_operator': item[1]})
                    print(item[1])

                # This will check for an integer
                if item[0] == 'INTEGER' or item[0] == 'STRING':
                    #TODO Create an add to the syntax tree
                    ast['ConditionalStatement'].append({'value': item[1]})
                    print(item[1])
                    
                print(item)
                print(ast)

    

    def find_variable_scope(self):
        """ Find/set variable scope

        This will set or find the scope of a variable being declared or called
        so that it can create a list of priorotised variables which should be called.
        """
        print('Find it by looping through source_ast and sorting through _scope tagged names')

    

    def does_var_exist(self, name):
        """ Check to see if a variable exists 

        This will perform semantical analysis by checking if a dclared variable already exists

        Args:
            name (str) : The name of the variable to check
        Return:
            bool :       'True' if it already exists and 'False' if it doesn't 
        """
        for x in self.symbol_tree:
            if x[0] == name: return True
        return False


    
    def parse_variable_decleration(self, token_stream, found_at_index):
        """ Parsing Variable decleration

        This will parse through a variable decleration and create it's abstract tree and handle any
        syntax errors

        Args:
            token_stream (list) : List of tokens starting from where if statement was found

        Returns:
            AST : The variable decleration abstract syntax tree
        """

        # Will hold the vraible decleration abstract syntax tree being built
        ast = []
        # Keeps track of the index within variable decleration
        index = 0

        for item in token_stream:
            
            # This will add one every loop to the index of the var decleration
            index += 1

            # This will get the variable type and add it to the AST
            if index == 1: ast.append({ 'VariableDeclerator': [ {'type': item[1]} ]})
            
            # This will check for the variable name
            if index == 2:
                
                # This wll check if the variable name already exists
                if self.does_var_exist(item[1]) == False:
                    # This will check to make sure that the name of the doesn't start wih a number
                    if not item[1][0].isdigit(): ast[0]['VariableDeclerator'].append({ 'name': item[1] })
                    # This will print an error if variable begins with a number
                    else: print('Illegal Variable Name "' + item[1] + '" variable name cannot begind with a number')
               
                # if there was an error then print it and then quit
                else:
                    print('Error: Variable name "' + item[1] + '" is already defined!')
                    quit()

            
            # This will check for equal sign
            if index == 3: 
                if item[1] == '=': pass
                # if there was an error then print it and then quit
                else: 
                    print("SyntaxError: An equal sign '=' was excpexted in variable decleration")
                    quit()

            # This will check the variable value but will skip the equal sign
            if index >= 4 and item[1] != ';':
                # TODO Modify this code to allow for more complex var declerations

                # Check if the value is the same value as the datatype in decleration
                if str(type(literal_eval(item[1]))) == "<class " + "'" + ast[0]['VariableDeclerator'][0]['type'] + "'>":
                    ast[0]['VariableDeclerator'].append({ 'value': item[1] })

               # if there was an error then print it and then quit
                else: 
                    print("TypeError: Variable value does not conform to data type of " + str(type(literal_eval(item[1]))))
                    quit()
                
            # If the for loop reaches the end statement then break because it is the end of the var decleration
            if item[1] == ';': break
        
        # Append this var declerating ast to the complete source ast and symbol table
        self.source_ast['main_scope'].append(ast[0])
        self.symbol_tree.append( [ ast[0]['VariableDeclerator'][1]['name'], ast[0]['VariableDeclerator'][2]['value'] ] )



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