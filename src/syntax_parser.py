#
#  Tachyon
#  syntatic_parsing.py
#
#  Created on 03/06/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import constants # for constants like tachyon keywords and datatypes
from ast import literal_eval # for getting type of variable decleration of value

class SyntaxParser(object):


    
    def __init__(self, token_stream):
        # Complete Abstract Syntax tree
        self.source_ast = { 'main_scope': [] }
        # Symbol table fo variable semantical analysis
        self.symbol_tree = [ ['last_name', 'Maugin'], ['test', 'test101'] ]
        # This will hold all error messages
        self.error_messages = []
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
            
            # This will find the token pattern for a variable decleration
            if token_type == "DATATYPE":
                self.variable_decleration_parsing(token_stream[self.token_index:len(token_stream)])
                
            # This will find the token pattern for an if statement
            elif token_type == "IDENTIFIER" and token_value == "if":
                print("IF STATEMENT FOUND")

            self.token_index += 1
        
        # Check if there were any errors and if so display them all
        if self.error_messages != []: self.send_error_message(self.error_messages)
        
        print(self.source_ast)


    
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
            # This will handle error detection for making sure the '=' is found
            if x == 2 and token_type != "OPERATOR" and token_value != "=":
                self.error_messages.append(["Variable Decleration Missing '='.", self.token_stream[self.token_index:self.token_index + tokens_checked + 1] ])

            # If a statement end is found then break out parsing
            if token_stream[x][0] == "STATEMENT_END": break

            # This will parse the first token which will be the var type
            if x == 0: ast['VariableDecleration'].append({ "type": token_value })

            # This will parse the second token which will be the name of the var
            if x == 1 and token_type == "IDENTIFIER":
                
                # Check if a variable has already been named the same and is so send an error
                if self.get_variable_value(token_value) != False:
                    self.error_messages.append(["Variable '%s' already exists and cannot be defined again!" % token_value, self.token_stream[self.token_index:self.token_index + tokens_checked + 1] ])
                else: 
                    ast['VariableDecleration'].append({ "name": token_value })

            # Error handling for variable name to make sure naming convention is acceptable
            if x == 1 and token_type != "IDENTIFIER":
                self.error_messages.append(["Invalid Variable Name '%s'" % token_value, self.token_stream[self.token_index:self.token_index + tokens_checked + 1] ])

            # This will parse the 3rd token which is the value of the variable
            if x == 3 and token_stream[x + 1][0] == "STATEMENT_END":

                # Check if the value matches the variable defined type
                if type(eval(token_value)) == eval(token_stream[0][1]):
                    # Add value as a number not a string if it is an int or else add it as a string
                    try: ast['VariableDecleration'].append({ "value": int(token_value) })
                    except ValueError: ast['VariableDecleration'].append({ "value": token_value })
                else:
                    self.error_messages.append(["Variable value does not match defined type!", 
                                                self.token_stream[self.token_index:self.token_index + tokens_checked + 1] ])

            # This will parse any variable declerations which have concatenation or arithmetics
            elif x >= 3:

                # Holds the list of ints and perands that will be passed to equation parser
                value_list = []

                for equation_item in range(x, len(token_stream)):
                    # If there is an end statement then break because the var decl is done
                    if token_stream[equation_item][0] == "STATEMENT_END": break

                    # Try to append item as int not string if you can
                    try:               value_list.append(int(token_stream[equation_item][1]))
                    except ValueError: value_list.append(token_stream[equation_item][1])

                    tokens_checked += 1 # Indent the tokens checked within this for loop

                # Call the equation parser and append value returned or try concat parser if an error occurs
                try: ast['VariableDecleration'].append({ "value": self.equation_parser(value_list)})
                except:
                    try:    ast['VariableDecleration'].append({ "value": self.concatenation_parser(value_list) })
                    except: self.error_messages.append(["Invalid variable decleration!", self.token_stream[self.token_index:self.token_index + tokens_checked] ])
                break                   # Break out of the current var parsing loop since we just parsed everything

            tokens_checked += 1         # Indent within overall for loop

        try: ast['VariableDecleration'][0] 
        except: self.error_messages.append(["Invalid variable decleration coud not set variable type!", self.token_stream[self.token_index:self.token_index + tokens_checked] ])
        try: ast['VariableDecleration'][1]
        except: self.error_messages.append(["Invalid variable decleration coud not set variable name!", self.token_stream[self.token_index:self.token_index + tokens_checked] ])
        try: ast['VariableDecleration'][2]
        except: self.error_messages.append(["Invalid variable decleration coud not set variable value!", self.token_stream[self.token_index:self.token_index + tokens_checked] ])

        self.source_ast['main_scope'].append(ast)
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
                else: self.error_messages.append(["Error parsing equation, check that you are using correct operand",
                                                 equation])

            # Skip every number since we already check and use them
            elif item % 2 == 0: pass
        
        return total



    def concatenation_parser(self, concatenation_list):
        """ Concatenaion Parser

        This will parse concatenation of strings and variables with string values or integer
        values to concatenate arithmetics to strings e.g. "Ryan is ", 10 + 6, "!"

        args:
            concatenation_list (list) : Array with all items needed seperated to perform concatenation
        return:
            value (string)            : Full string after concatenation done
            error (list)              : Return False with an error message in a list
        """

        full_string = ""

        for item in range(0, len(concatenation_list)):
            
            current_value = concatenation_list[item]

            # Add the first item to the string
            if item == 0:
                
                # This checks if the value being checked is a string or a variable
                # If it is a string then just add it without the surrounding quotes
                if current_value[0] == '"': full_string += current_value[1:len(current_value) - 1]
                # If it isn't a string then get the variable value and append it
                else: full_string += self.get_variable_value(current_value)
                pass
            
            # This will check for the concatenation operator
            if item % 2 == 1:
                if current_value == "+": 
                    # This checks if the value being checked is a string or a variable
                    if concatenation_list[item + 1][0] != '"': full_string += self.get_variable_value(concatenation_list[item + 1])
                    else: full_string += concatenation_list[item + 1][1:len(concatenation_list[item + 1]) - 1]
                        
                elif current_value == ",": 
                    full_string += " " + concatenation_list[item + 1]

                else: self.error_messages.append(["Error parsing equation, check that you are using correct operand",
                                                 concatenation_list])
            
            # This will skip value as it is already being added and dealt with when getting the operand
            if item % 2 == 0: pass

        return full_string



    def get_variable_value(self, name):
        """ Get Variable Value

        This will get the value of a variable from the symbol tree and return the value
        if the variable exists or an error if it doesn't

        args:
            name (string)  : The name which we will search for in symbol tree
        returns:
            value (string) : The value of the variable if it is found
            error (bool)   : Sends back False if it was not found
        """

        for var in self.symbol_tree:
            if var[0] == name: return var[1]
        return False



    def send_error_message(self, error_list):
        print("------------------------ %s ERROR'S FOUND ------------------------" % len(error_list))
        for error in range(0, len(error_list)):
            print("%s)  %s" % (error, error_list[error][0]))
            print('    ' + '\033[91m' + " ".join(str(x) for x in error_list[error][1]) + '\033[0m')
        print("-----------------------------------------------------------------")
        quit()