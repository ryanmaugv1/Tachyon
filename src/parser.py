#
#  Tachyon
#  Parser.py
#
#  Created on 03/06/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import constants # for constants like tachyon keywords and datatypes

class Parser(object):



    def __init__(self, token_stream):
        # Complete Abstract Syntax tree
        self.source_ast = { 'main_scope': [] }
        # Symbol table fo variable semantical analysis
        self.symbol_tree = [ ['last_name', 'Maugin'], ['test', 'test101']]
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
                self.variable_decleration_parsing(token_stream[self.token_index:len(token_stream)], False)
                
            # This will find the token pattern for an if statement
            elif token_type == "IDENTIFIER" and token_value == "if":
                self.conditional_statement_parser(token_stream[self.token_index:len(token_stream)], False)

            # This will find the pattern for a buil-in function call
            elif token_type == "IDENTIFIER" and token_value in constants.BUILT_IN_FUNCTIONS:
                self.parse_built_in_function(token_stream[self.token_index:len(token_stream)], False)

            self.token_index += 1
        
        # Check if there were any errors and if so display them all
        if self.error_messages != []: self.send_error_message(self.error_messages)

        print(self.source_ast)
        return self.source_ast
    


    def parse_built_in_function(self, token_stream, isInBody):
        """ Parse Built-in Function 
        
        This is will parse built in methods and their parameters to form AST
        """

        ast = {'PrebuiltFunction': []}
        tokens_checked = 0

        for token in range(0, len(token_stream)):
            
            if token == 0:
                ast['PrebuiltFunction'].append( {'type': token_stream[token][1]} )
            if token == 1 and token_stream[token][0] in ['INTEGER', 'STRING', 'IDENTIFIER']:

                # If the argument passed is a variable (identifier) then try get value
                if token_stream[token][0] == 'IDENTIFIER':
                    # Get value and handle any errors
                    value = self.get_variable_value(token_stream[token][1])
                    if value != False: 
                        ast['PrebuiltFunction'].append( {'arguments': [value]} )
                    else: 
                        self.error_messages.append([ "Variable '%s' does not exist" % token_stream[tokens_checked][1], 
                                                    token_stream[0:tokens_checked + 1] ])

                # TODO Allow for concatenation and equation parsing
                else: ast['PrebuiltFunction'].append( {'arguments': [token_stream[token][1]]} )

            tokens_checked += 1

        # If it's being parsed within a body don't ass the ast to the source ast
        if not isInBody: self.source_ast['main_scope'].append(ast)
        # Increase token index to make up for tokens checked
        self.token_index += tokens_checked 
        
        return [ast, tokens_checked]


    
    def variable_decleration_parsing(self, token_stream, isInBody):
        """ Variable Decleration Parsing

        This method will parse variable declerations and add themto the source AST

        Args:
            token_stream (list) : The token stream starting from where var decleration was found
        """

        ast = { 'VariableDecleration': [] }  # The abstract syntax tree for var decl
        tokens_checked = 0                   # Number of token checked that made up the var decl
        var_exists = True

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
                    var_exists = False # Set var exists to False so that it can be added
                    ast['VariableDecleration'].append({ "name": token_value })

            # Error handling for variable name to make sure the naming convention is acceptable
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

        # Last case error validation checking if all needed var decl elements are in ast such as:
        # var type, name and value
        try: ast['VariableDecleration'][0] 
        except: self.error_messages.append(["Invalid variable decleration coud not set variable type!", self.token_stream[self.token_index:self.token_index + tokens_checked] ])
        try: ast['VariableDecleration'][1]
        except: self.error_messages.append(["Invalid variable decleration coud not set variable name!", self.token_stream[self.token_index:self.token_index + tokens_checked] ])
        try: ast['VariableDecleration'][2]
        except: self.error_messages.append(["Invalid variable decleration coud not set variable value!", self.token_stream[self.token_index:self.token_index + tokens_checked] ])

        # If this is being run to parse inside a body then there is no need to add it to the source ast
        # as it will be added to the body of statement being parsed
        if not isInBody:
            self.source_ast['main_scope'].append(ast)

        # Add varible name and value to symbol tree and increase token index
        if not var_exists:
            self.symbol_tree.append( [ast['VariableDecleration'][1]['name'], ast['VariableDecleration'][2]['value']] )
        self.token_index += tokens_checked

        return [ast, tokens_checked] # Return is only used within body parsing to create body ast




    def conditional_statement_parser(self, token_stream, isNested):
        """ Conditional Statement Parser

        This will parse conditional statements like 'if else' and create an
        abstract sytax tree for it.

        args:
            token_stream: tokens which make up the conditional statement
        """

        tokens_checked = 0
        ast = {'ConditionalStatement': []}

        # This loop will parse the condition e.g. if 12 < 11
        for x in range(0, len(token_stream)):
            tokens_checked += 1

            # Simplification variables that will improve readbility
            token_type  = token_stream[x][0]
            token_value = token_stream[x][1]
            allowed_conditional_token_types = ['INTEGER', 'STRING', 'IDENTIFIER']

            # Break out of loop at the end of the condition
            if token_type == 'SCOPE_DEFINER' and token_value == '{': break

            # Pass if token is the 'if' identifier as it has already been checked
            if token_type == 'IDENTIFIER' and  token_value == 'if':  pass

            # This will check for the first value and add it to the AST
            if x == 1 and token_type in allowed_conditional_token_types:
                # This will check for an identifier (var) and then check if it exists so it can add the value to it
                if self.get_variable_value(token_value) != False:
                    ast['ConditionalStatement'].append( {'value1': self.get_variable_value(token_value)} )
                else:
                    ast['ConditionalStatement'].append( {'value1': token_value} )

            # This will check for the comparison operator and add it to the AST
            if x == 2 and token_type == 'COMPARISON_OPERATOR':
                ast['ConditionalStatement'].append( {'comparison_type': token_value} )

            # This will check for the second value and add it to the AST
            if x == 3 and token_type in allowed_conditional_token_types:
                # This will check for an identifier (var) and then check if it exists so it can add the value to it
                if self.get_variable_value(token_value) != False:
                    ast['ConditionalStatement'].append( {'value2': self.get_variable_value(token_value)} )
                else:
                    ast['ConditionalStatement'].append( {'value2': token_value} )

        # Increment global token index for tokens checked in condition
        self.token_index += tokens_checked

        # Get condition statament details
        comparison_type = ast['ConditionalStatement'][1]['comparison_type']
        values          = [ ast['ConditionalStatement'][0]['value1'], ast['ConditionalStatement'][2]['value2'] ]

        # Check if condition is true or false and add result to AST
        if self.perform_conditional_checks(comparison_type, values, tokens_checked):
            # This will get the body tokens and the tokens checked that make up the body to skip them
            get_body_return = self.get_statement_body(token_stream[tokens_checked:len(token_stream)])

            # If it nested then call parse_body with nested parameter of true else false
            if isNested == True: self.parse_body(get_body_return[0], ast, True)
            else: self.parse_body(get_body_return[0], ast, False)

            # Add the amount tokens we checked in body 
            tokens_checked += get_body_return[1]

        return [ast, tokens_checked] # Return is only used within body parsing to create body ast



    def parse_body(self, token_stream, statement_ast, isNested):
        """ Parse body

        This will parse the body of conditional, iteration, functions and more in order
        to return a body ast like this --> {'body': []}

        args:
            token_stream (list) : tokens which make up the body
        returns:
             ast       (object) : Abstract Syntax Tree of the body
        """
        
        ast = {'body': []}
        tokens_checked = 0

        # Loop through each token to find a pattern to parse
        while tokens_checked < len(token_stream):

            # This will parse variable declerations within the body 
            if token_stream[tokens_checked][0] == "DATATYPE":
                var_decl_parse = self.variable_decleration_parsing(token_stream[tokens_checked:len(token_stream)], True)
                ast['body'].append(var_decl_parse[0])
                tokens_checked += var_decl_parse[1]
            
            # This will parse nested conditional statements within the body
            elif token_stream[tokens_checked][0] == 'IDENTIFIER' and token_stream[tokens_checked][1] == 'if':
                condition_parsing = self.conditional_statement_parser(token_stream[tokens_checked:len(token_stream)], True)
                ast['body'].append(condition_parsing[0])
                tokens_checked += condition_parsing[1] - 1 # minus one to not skip extra token

            elif token_stream[tokens_checked][0] == 'IDENTIFIER' and token_stream[tokens_checked][1] in constants.BUILT_IN_FUNCTIONS:
                built_in_func_parse = self.parse_built_in_function(token_stream[self.token_index:len(token_stream)], True)
                ast['body'].append(built_in_func_parse[0])
                tokens_checked += built_in_func_parse[1]

            tokens_checked += 1
        
        # Form the full ast with the statement and body combined and then add it to the source ast
        statement_ast['ConditionalStatement'].append(ast)
        # If the statments is not nested then add it or else don;t because parent will be added containing the child
        if not isNested: self.source_ast['main_scope'].append(statement_ast)


    
    def get_statement_body(self, token_stream):
        """ Get Statement Body 
        
        This will get the tokens that make up the body of a statement  and return 
        the tokens
        
        args:
            token_stream (list): This will hold the tokens after the scope definer
        return:
            tokens_list  (list): Returns tokens that make up the body for statement
        """

        nesting_count = 1
        tokens_checked = 0
        body_tokens = []

        for token in token_stream:
            
            tokens_checked += 1

            # Simpliies & Increases readabilty of toke type and value
            token_value = token[1]
            token_type  = token[0] 

            # Keeps track of the opening and closing scope definers '}' and '{'
            if token_type == "SCOPE_DEFINER" and token_value == "{": nesting_count += 1
            elif token_type == "SCOPE_DEFINER" and token_value == "}": nesting_count -= 1
            
            # Checks whether the closing scope definer is found to finish creating body tokens
            if nesting_count == 0: break
            else: body_tokens.append(token)

        return [body_tokens, tokens_checked]
    

    def perform_conditional_checks(self, comparison_type, values, tokens_checked):
        """ Perform Conditional Checks

        This will perform the condtitional checks and see whether the condition evaluates
        to true or false

        args:
            comparison_type (str) : The comparison operator e.g ==, < or >=
            values         (list) : The values that comparison will be applied on
        return:
            boolean               : True or False based on condition evaluation
        """

        if comparison_type == '==':
            if values[0] == values[1]: return True
            else: return True
        elif comparison_type == '!=':
            if values[0] != values[1]: return True
        elif comparison_type == '>':
            try:
                if int(values[0]) > int(values[1]): return True
                else: return True
            except: self.error_messages.append(["ERROR: Cannot perform comparison check '>' on string values",
                                               self.token_stream[self.token_index:self.token_index + tokens_checked] ])
        elif comparison_type == '<':
            try:
                if int(values[0]) < int(values[1]): return True
                else: return True
            except: self.error_messages.append(["ERROR: Cannot perform comparison check '<' on string values",
                                               self.token_stream[self.token_index:self.token_index + tokens_checked] ])
        elif comparison_type == '>=':
            try:
                if int(values[0]) >= int(values[1]): return True
                else: return True
            except: self.error_messages.append(["ERROR: Cannot perform comparison check '>=' on string values",
                                               self.token_stream[self.token_index:self.token_index + tokens_checked] ])
        elif comparison_type == '<=':
            try:
                if int(values[0]) <= int(values[1]): return True
                else: return True
            except: self.error_messages.append(["ERROR: Cannot perform comparison check '<=' on string values",
                                               self.token_stream[self.token_index:self.token_index + tokens_checked] ])


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

        return '"' + full_string + '"'



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
        """ Send Error Messages

        This will simply send all the found error messages within the source code
        and return a list of error messages and tokens of which part of the source code
        caused that error

        args:
            error_list (list) : List with error message and tokens
        """
        
        print("------------------------ %s ERROR'S FOUND ------------------------" % len(error_list))
        for error in range(0, len(error_list)):
            print("%s)  %s" % (error, error_list[error][0]))
            print('    ' + '\033[91m' + " ".join(str(x) for x in error_list[error][1]) + '\033[0m')
        print("-----------------------------------------------------------------")
        quit()