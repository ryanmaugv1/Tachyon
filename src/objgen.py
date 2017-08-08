#
#  Tachyon
#  objgen.py
#
#  Created on 06/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

class ObjectGenerator():


    def __init__(self, source_ast):
        # This will contain all the AST's in forms of dictionaries to help with creating AST object
        self.source_ast = source_ast


    def object_definer(self):
        """ Object Definer 
        
        This method will find all the different objects and call all the objects
        and pass in the ast dictionary to them to get a python string of code back
        which transpiles the tachyon source code into python
        
        returns:
            python_code (str) : This will written a string of python code
        """
        print(self.source_ast)