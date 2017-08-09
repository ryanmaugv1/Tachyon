#
#  Tachyon
#  varObject.py
#
#  Created on 09/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

class VaribleObject():

    def __init__(self, ast):
        # The ast will hold the dictionary version of the ast which is like a blueprint
        self.ast = ast

    
    def transpile(self):
        """ Transpile 
        
        This method will use the AST in order to create a python version of the tachyon
        generated dictionary AST.
        """
        print(self.ast)