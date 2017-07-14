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
            
           
            # This will parse any variable declerations which have concatenation or arithmetics
            elif x >= 3:

                value_list = [] # Holds the list of ints and perands that will be passed to equation parser

                for equation_item in range(x, len(token_stream)):
                    # If there is an end statement then break because the var decl is done
                    if token_stream[equation_item][0] == "STATEMENT_END": break

                    # Try to append item as int not string if you can
                    try:               value_list.append(int(token_stream[equation_item][1]))
                    except ValueError: value_list.append(token_stream[equation_item][1])

                    tokens_checked += 1 # Indent the tokens checked within this for loop

                # Call the equation parser and append value of successful or try tring concat parser if an error occurs
                try:    ast['VariableDecleration'].append({ "value": self.equation_parser(value_list) })
                except: print("Use string concat var value parsing")
                break                   # Break out of the current var parsing loop since we just parsed everything

            tokens_checked += 1         # Indent within overall for loop
        
        print(ast)
        self.token_index += tokens_checked
    


    def equation_parser(self, equation):
        """ Equation parsing

        This will parse equations such as 10 * 10 which comes in as an array with nums
        and operands

        args:
            equation (list) : List of the ints and operands in order
        returns:
            value (int)     : The value of the equation 
        """
        total = 0 # Holds equation value

        for item in range(0, len(equation)):
            
            # Add first value to total as a starting int to perform calculatios on
            if item == 0:
                total += equation[item]
                pass

            # This will check every operator and perform the right calculations based on total
            # and the number that is after the operator
            if item % 2 == 1:
                if equation[item] == "+": total += equation[item + 1]
                elif equation[item] == "-": total += equation[item + 1]
                elif equation[item] == "/": total /= equation[item + 1]
                elif equation[item] == "*": total *= equation[item + 1]
                elif equation[item] == "%": total %= equation[item + 1]
                else: print("Invalid Operator")

            # Skip every number since we already check and use them
            elif item % 2 == 0: pass
        
        return total
        