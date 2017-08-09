# Object Generation

All object generation will be done within the `objgen.py` file and what it simply does is call different objects (classes) which will produce a string of python code and return it. After having done thatsequentially with all the ordered AST dictionaries we should get the python equivelant transpilation of tachyon code which we can just execute using the `exec()` function.

First of what happens in the `objgen.py` file is we initialise the `ObjectGenerator` class with one argument which is `source_ast` which will be the ordered list of ast dictionaries. We then create 2 variables called `source_ast` and `exec_string` which will hold the tachyon to python transpiled code.

    class ObjectGenerator():
    
        def __init__(self, source_ast):
            # This will contain all the AST's in forms of dictionaries to help with creating AST object
            self.source_ast  = source_ast['main_scope']
            # This will hold the executable string of transplied tachyon code to python
            self.exec_string = ""

Next, the `object_definer` method is created which is the method which is the main method of the `ObjectGenerator` class. This method will find all the different ast objects within the ast dictionary and call all the objects and pass in the ast dictionary to get a python string of code back which is the tachyon code transpiled into python.

    def object_definer(self):
        """ Object Definer 
        
        This method will find all the different ast objects within the ast dictionary
        and call all the objects and pass in the ast dictionary to get a python 
        string of code back which is the tachyon code transpiled into python
        
        returns:
            python_code (str) : This will written a string of python code
        """
        
        # Iterate through all ast dictionaries
        for ast in self.source_ast:
            # This will check check if the current AST dict is of which type
            if self.check_ast('VariableDecleration', ast):
                print('var')

            if self.check_ast('ConditionalStatement', ast):
                print('condition')

            if self.check_ast('PrebuiltFunction', ast):
                print('prebuilt')

However, within the `object_definer` method there are calls to the `check_ast` which it’s role is to check if the current AST's dictionary items being looped through haa the same key as the `astName` argument passed in. The main reason for this method is so that the `object_definer` method looks more cleaner, readable and doesn't perform repetition.

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