#
#  Tachyon
#  varObject.py
#
#  Created on 09/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

class VariableObject():

    def __init__(self, ast):
        # The ast will hold the dictionary version of the ast which is like a blueprint
        self.ast = ast['VariableDecleration']
        # This will hold the exec string for variable decleration
        self.exec_string = ""

    
    def transpile(self):
        """ Transpile 
        
        This method will use the AST in order to create a python version of the tachyon
        generated dictionary AST.

        return:
            exec_string (str) : The python transpiled code
        """
        
        # Loop through each dictionary value items
        for val in self.ast:
            
            # Get the name of the variable
            try: self.exec_string += val['name'] + " = "
            except: pass

            # Get the value of the variable
            try: self.exec_string += str(val['value'])
            except: pass

        return self.exec_string