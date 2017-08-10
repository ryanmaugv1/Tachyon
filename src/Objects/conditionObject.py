#
#  Tachyon
#  conditionObject.py
#
#  Created on 09/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import objgen

class ConditionObject():

    def __init__(self, ast):
        # The ast will hold the dictionary version of the ast which is like a blueprint
        self.ast = ast['ConditionalStatement']
        # This will hold the exec string for variable decleration
        self.exec_string = ""


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
            try:
                print(val['body'])
            except: pass
        
        print(self.exec_string)
        return self.exec_string