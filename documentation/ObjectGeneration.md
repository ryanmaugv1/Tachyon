# Object Generation

All object generation will be done within the `objgen.py` file and what it simply does is call different objects (classes) which will produce a string of python code and return it. After having done that sequentially with all the ordered AST dictionaries we should get the python equivelant transpilation of the tachyon code which we can just execute using the `exec()` function.

First of what happens in the `objgen.py` file is we initialise the `ObjectGenerator` class with one argument which is `source_ast` which will be the ordered list of ast dictionaries. We then create 2 variables called `source_ast` and `exec_string` which will hold the tachyon to python transpiled code.

    class ObjectGenerator():
    
        def __init__(self, source_ast):
            # This will contain all the AST's in forms of dictionaries to help with creating AST object
            self.source_ast  = source_ast['main_scope']
            # This will hold the executable string of transplied tachyon code to python
            self.exec_string = ""

Next, the `object_definer` method is created which is the main method of the `ObjectGenerator` class. This method will find all the different ast objects within the ast dictionary and call all the objects and pass in the ast dictionary to get a python string of transpiled python code back.

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

## Body Code Generation

> This is a crucial part of the object generation stage for statement which need have their own scope/body code e.g. **`Forloops`**, **`ConditionalStatement`**, **`Functions`**, and **`WhileLoops`** AST's all make use of body code generation.

The body generation for a statement is done in the `transpile_body` method which makes use of other methods such as:

- `check_ast`
    - This method will check if the AST dictionary item being looped through has the same key name as the `astName` argument to see deterine what ast type is being looped through.
- `should_dedent_trailing`
    - This method will check if the ast item being checked is outside a conditional statement.
- `should_increment_nest_count`
    - This method will check if another statement is found and whether or not it should increase nesting count.

What the transpile body does is what the `objen.py - object_definer()` method does which just creates objects from the AST found but the body code generation differs because it handles indentation too.

The following code snippet shows how the objects are being generated within the body of a statement. It is very similar to the way it is done in the `objgen.py` file but as you can see it also handles nestings (indentation).

    # This will parse comments within the body
    if self.check_ast('Comment', ast):
        gen_comment = CommentObject(ast)
        transpile = gen_comment.transpile()
        if self.should_dedent_trailing(ast, self.ast):
            body_exec_string += ("   " * (nesting_count - 1)) + transpile + "\n"
        else:
            body_exec_string += ("   " * nesting_count) + transpile + "\n"

The following code snippet is a bit more different as it is generating a for loop which has a statement and body of it's own which both need to be at different indentations therefore it handles the need to decrement when finishing the indentation for a certain statement etc using the methods we spoke about above. Conditional statement, for loops, function declerations all have this same concept applied to them.

    # This will parse nested conditional statement within the body
    if self.check_ast('ForLoop', ast):
        # Increase nesting count because this is a condition statement inside a conditional statement
        # Only increase nest count if needed
        if self.should_increment_nest_count(ast, self.ast):
            nesting_count += 1
        # Create conditional statement exec string
        loop_obj = LoopObject(ast, nesting_count)
        # The second nested statament only needs 1 indent not 2
        if nesting_count == 2: 
            # Add the content of conditional statement with correct indentation
            body_exec_string += "   " + loop_obj.transpile()
        else: 
            # Add the content of conditional statement with correct indentation
            body_exec_string += ("   " * (nesting_count - 1)) + loop_obj.transpile()






















