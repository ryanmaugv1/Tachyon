#
#  Tachyon
#  conditionObject.py
#
#  Created on 09/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import objgen
from Objects.varObject     import VariableObject
from Objects.builtinObject import BuiltInFunctionObject

class ConditionObject():

    def __init__(self, ast, nesting_count):
        # The ast will hold the dictionary version of the ast which is like a blueprint
        self.ast = ast['ConditionalStatement']
        # This will hold the exec string for variable decleration
        self.exec_string = ""
        # This is to handle the nesting indentation
        self.nesting_count = nesting_count


    def transpile(self):
        """ Transpile 
        
        This method will use the AST in order to create a python version of the tachyon
        generated dictionary AST.

        return:
            exec_string (str) : The python transpiled code
        """

        # Loop through each ast value list items
        for val in self.ast:

            # Get the first comparison value
            try: self.exec_string += "if " + str(val['value1']) + " "
            except: pass

            # Get the comparison type
            try: self.exec_string += val['comparison_type'] + " "
            except: pass

            # Get the second comparison valie
            try: self.exec_string += str(val['value2']) + ": \n"
            except: pass

            # Get the body of the conditional statement
            try: self.exec_string += self.transpile_body(val['body'], self.nesting_count)
            except: pass
        
        return self.exec_string


    def transpile_body(self, body_ast, nesting_count):
        
        # Holds the body executable string of the first statement
        body_exec_string = ""
        
        # Loop through each ast item in the body dictionary
        for ast in body_ast:
            
            # This will parse variable declerations within the body
            if self.check_ast('VariableDecleration', ast):
                var_obj = VariableObject(ast)
                body_exec_string += ("   " * nesting_count) + var_obj.transpile() + "\n"
            
            # This will parse nested conditional statement within the body
            if self.check_ast('ConditionalStatement', ast):
                # Increase nesting count because this is a condition statement inside a conditional statement
                nesting_count += 1
                # Create conditional statement exec string
                condition_obj = ConditionObject(ast, nesting_count)
                # The second nested statament only needs 1 indent not 2
                if nesting_count == 2: 
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += "   " + condition_obj.transpile()
                else: 
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += ("   " * (nesting_count - 1)) + condition_obj.transpile()
                    
            # This will parse built-in within the body
            if self.check_ast('PrebuiltFunction', ast):
                gen_builtin = BuiltInFunctionObject(ast)
                body_exec_string += ("   " * nesting_count) + gen_builtin.transpile() + "\n"
        
        return body_exec_string

    
    def check_ast(self, astName, ast):
        """ Call and Set Exec 
        
        This method will check if the AST dictionary item being looped through has the
        same key name as the `astName` argument
        
        args:
            astName (str)  : This will hold the ast name we are matching
            ast     (dict) : The dict which the astName match will be done against
        returns:
            True    (bool) : If the astName matches the one in `ast` arg
            False   (bool) : If the astName doesn't matches the one in `ast` arg
        """
        try:
            if ast[astName]: return True
        except: return False