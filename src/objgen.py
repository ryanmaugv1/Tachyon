#
#  Tachyon
#  objgen.py
#
#  Created on 06/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

# Import all the objects
from Objects.varObject       import VariableObject
from Objects.conditionObject import ConditionObject
from Objects.builtinObject   import BuiltInFunctionObject

class ObjectGenerator():


    def __init__(self, source_ast):
        # This will contain all the AST's in forms of dictionaries to help with creating AST object
        self.source_ast  = source_ast['main_scope']
        # This will hold the executable string of transplied tachyon code to python
        self.exec_string = ""


    def object_definer(self, isGettingBody):
        """ Object Definer 
        
        This method will find all the different ast objects within the ast dictionary
        and call all the objects and pass in the ast dictionary to get a python 
        string of code back which is the tachyon code transpiled into python
        
        returns:
            python_code (str) : This will written a string of python code
        """
        
        # Iterate through all ast dictionaries
        for ast in self.source_ast:

            # Create dictionary var object and append exec string global exec string
            if self.check_ast('VariableDecleration', ast):
                gen_var = VariableObject(ast)
                self.exec_string += gen_var.transpile() + '\n'

            # Create dictionary condition object and append exec string global exec string
            if self.check_ast('ConditionalStatement', ast):
                gen_condition = ConditionObject(ast, 1)
                self.exec_string += gen_condition.transpile() + '\n'

            # Create dictionary builtin object and append exec string global exec string
            if self.check_ast('PrebuiltFunction', ast):
                gen_builtin = BuiltInFunctionObject(ast)
                self.exec_string += gen_builtin.transpile() + "\n"

        return self.exec_string


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