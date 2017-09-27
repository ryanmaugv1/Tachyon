# **Parser**

> This documentation file for parser will soon be populated with clear pictures from notebook where all documentation has been done in detail with diagrams.

---

## Class Parser

The parser class will handle all the syntatic and semantical analysis of the the parsing for the code. It will also raise errors when syntax errors are found.

### Parser class initialisers:

- `source_ast`

    This will initiall hold a dictionary with the key of `main_scope` with the value of an empty array where all the source code AST structures will be appended to. This will be used in order to be interpreted and compiled. The variable will look like this: `{'main_scope': []}`.

- `symbol_tree`

    This will be used in order to store variables with their name and value in the following format `['name', 'value']` so that I can perform semantical analysis and perform checks to see if a variable exists or not.

- `token_stream`

    This will hold the tokens that have just been produced by the lexical analyser which the parser will use to turn into an Abstract Syntax Tree (AST) and Symbol Trees so that syntatic and semantical analysis can be performed.

- `error_messages`

    This will hold all the error messages that happened during the parsing and print them all out at the end of the source code parsing if there are any.

- `token_index`

    This holds the index of the tokens which we have checked globally so that we can keep track of the tokens we have checked.

---

## `parse()`

This will parse the tokens given as argument and turn the sequence of tokens into abstract syntax trees.

**Arguments**

- `token_stream (list)`
    - The tokens produced by lexer

**Returns**

- `source_ast (dict)`
    - This will return the full source code ast

This method tries to identifiy a pattern of tokens that make up a parse tree for example a variable would be recognised if the parse method stumbled across a datatype token (`['DATATYPE', 'str']`) it would know it is a variable decleration and call the `variable_decleration_parsing()` passing in the token stream from where the data type was found with the rest of the tokens and will also pass in false because this parsing isn't called from a body statement parser. This is how it looks in code:

    if token_type == "DATATYPE":
        self.variable_decleration_parsing(token_stream[self.token_index:len(token_stream)], False)
          
This is then repeated for for all the tokens in the source code to find patterns and create AST's from them. Once all this is done the method checkd for an error messages like such:

    if self.error_messages != []: 
        self.send_error_message(self.error_messages)
        
This checks if the error message array is empty and if so no errors occured during parsing but if there is then error messages will all be displayed in hierachy order from first to last.

Finally, the method then returns the `source_ast` so that it can then be used by the ObjectGenerator (`objgen.py`) to make the Objects for the different AST's and transpile them into python.

---

## `parse_built_in_function()`

This will parse built in methods and their parameters to form an AST.

**Arguments**
- `token_stream (list)` 
    - The token stream starting from where the builtin function was found
- `isInBody (bool)`
    - This will hold True if this function is being run from body parsing

**Returns**

- `ast (dict)`
    - The condtion ast without the body
- `tokens_checked (int)`
    - The count of tokens checked that made up the condition statement

This methold will be called from the `parser()` or `parse_body()` method which will loop through the first token till it finds an `END_STATEMENT` token type which means it can then return the formed AST.

The method firstly starts off by creating two variables which are:

- **ast**
    - Which holds the AST e.g. `{'PrebuiltFunction': [{'type': 'print'}, {'param': ['Hello']}]}`
- **tokens_checked**
    - This variable holds the amount of tokens checked which make up the builtin function.

Next, I loop through each token passed in the `token_stream` and check for 3 token types and values at different indexes such as:

- The Prebuilt function type which is the name of the function e.g `print "Ryan";` the type will be `print` and this token has to be at token index 1.

      if token == 0:
          ast['PrebuiltFunction'].append( {'type': token_stream[token][1]} )

- At token index 2, I look for the parameter that is being passed in which has to be either a value like `string`, `int` or `bool` etc. Inside this check I also perform various operations lie getting the value of a variable if the the value passed is an `IDENTIFIER` (var) type.

      if token == 1 and token_stream[token][0] in ['INTEGER', 'STRING', 'IDENTIFIER']:
      
          # If the argument passed is a variable (identifier) then try get value
          if token_stream[token][0] == 'IDENTIFIER':
              # Get value and handle any errors
               value = self.get_variable_value(token_stream[token][1])
              if value != False: 
                  ast['PrebuiltFunction'].append( {'arguments': [value]} )
              else: 
                  self.error_messages.append([ "Variable '%s' does not exist" % token_stream[tokens_checked][1], token_stream[0:tokens_checked + 1] ])
                  
          else: 
              ast['PrebuiltFunction'].append( {'arguments': [token_stream[token][1]]} )

- Finally at the 3rd index I will be looking for a `STATEMENT_END` token type so that I know I can break out the loop so I don't check any more tokens. 

    `if token_stream[token][0] == "STATEMENT_END": break`
    
Once these checks are done and we hve exitted the loop I check whether this method was run from inside a body and if not then append the ast to the `source_ast` and increase `token_index` by adding the tokens checked count to it.

If the method is run with the `isInBody` being `True` then it will not append to the `source_ast` and will return it instead.

---

## `variable_decleration_parsing()`

This method will parse variable declerations and add them to the source AST or return them if variable decleration is being parsed for body of a statement.

**Arguments**
- `token_stream (list)`
    - The token stream starting from where the variable decleration was found
- `isInBody (bool)`
    - This will declare whether the var decleration is being parsed within a statement body.

**Returns**

- `ast (dict)`
    - The condtion ast without the body
- `tokens_checked (int)`
    - The count of tokens checked that made up the condition statement

To parse variable declerations what we do is get a list passed in as a parameter where the variable decleration starts. We also get a boolean value for `isInBody` to know if this variable decleration is parsed within a body.

Next I loop through all the tokens inside the `token_stream` and create a variable AST dictionary with the variable type, nam e and value until I find a `STATEMENT_END`token which means that the variable decleration is finished so I can then break out the loop.

Within the for loop I check for these things:

> `if x == 2 and token_type == "OPERATOR" and token_value == "=":`
This checks if the second token is a token of type `OPERATOR` and has the value of `=` and if so then we just `pass` but if not the we throw an error saying that the variable decleration is missing an equal sign (`=`).

> `if token_stream[x][0] == "STATEMENT_END":`
This will look for an `STATEMENT_END` token and when found will break out the loop as it is an indicator that the variable decleration is finished.

> `if x == 0:`
This will check for the type of the variable like `str`, `int` or `bool` etc. This won't need error detection as it will initiate the variable decleration parser so any else statement would never evaluate to true.

> `if x == 1 and token_type == "IDENTIFIER":`
This will get the name of the variable and inside will perform semantics check to make sure that a variable doesn't already exist with the same name.

> `if x == 3 and token_stream[x + 1][0] == "STATEMENT_END":`
This will parse the variable value if has only one token that makes up it's value or else the next example below is the one that will be called. What happens in this method is that the type assigned will be checked to make sure it matches declared type and then add the value to the AST.

> `elif x >= 3:`
This does the same as the above however it will handle variable value assignments that don't have just one simply value passed in but rather things like concatenation and equations e.g `int a = 10 + 10;`.

Once, I have broken out the loop I do some error checking to make sure that all the AST values needed are there or else I generate an error. I then check if the method was called with the parameter `isInBody` being `True` so I know whether to append the AST to the `source_ast` or not. I also perform some semantics validation by checking if the variable already exists by calling the `get_variable_value` method inside the loop when I find the name which should either return `False` or the value of the variable. Finally I simply increment the `token_index` by the number of tokens I checked through to make up the variable decleration and then return the `AST` and `tokens_checked` value.

---

## `conditional_statement_parser()`

> Conditional statement only support **one** condition checking and not two.

This will parse conditional statements like 'if else' and create an abstract sytax tree for it.

**Arguments**
- `token_stream (list)`
    - Tokens which make up the conditional statement
- `isNested (bool)`
    - **True** the conditional statement is being parsed within another conditional statement **False** if not.

**Returns**

- `ast (dict)`
    - The condtion ast without the body
- `tokens_checked (int)`
    - The count of tokens checked that made up the condition statement

What this method does is handle the parsing of conditional statements by tying in all the methods needed for thise which are `parse_body` and `get_statement_body`. The way conditions and the body of that conditional statement is parsed is seperate. 

The way the condition is parsed is simply by looping through the conditional statement getting the `first_value` followed by the `comparison_type` and finally the `second_value`. Once we got that the for loop should get a opening scope definer (`{`) which will then break and handle the parsing of the body seperately which is explained in more detail by the `parse_body` and `get_statement_body` documentation.

---

## `parse_body()`

This will parse the body of conditional, iteration, functions and more in order to return a body ast like this `{'body': []}`

**Arguments**
- `token_stream (list)`
    - Tokens which make up the body
- `statement_ast (dict)`
    - The condition of the body being parsed so the whole ast can be formed in this method and added to `source_ast`
- `isNested (bool)`
    - If the condition being parsed is nested

**Returns**
- `ast (object)`
    - Abstract Syntax Tree of the body

This method performs exactly what the `parse` method does but instead does for the bodies of statements only. The reason for this is because all the parse methods being called will return the AST & checked index count which is then used to append to a body ast which looks like this `{'body': []}` rather than the global `source_ast` variable. Once that's done and all the body AST's have been generated and added to the body AST it appends it to the `statement_ast` parameter which was passed in and appends it to the `source_ast` if the statement body being parsed wasn't nested because if it was then that wouldn't be the fulle conditional statement AST to add.

---

## `get_statement_body()`

This will get the tokens that make up the body of a statement and return the tokens.

**Arguments**
- `token_stream (list)`
    - This will hold the tokens after the scope definer

**Returns**
- `tokens_list (list)`
    - Returns tokens that make up the body for statement

What this method does is it gets passed a token stream which will always start from an opening scope definer such as `{` and from there it collects all of the body tokens for the statement e.g `Conditional Statement` or `Repetetive Statement`. It also acknowledges nesting because in order to break out the loop when it's collecting the body tokens it needs to find a closing scope definer such as `}` but if there is nesting then there would be errors which is why it also does nesting count. 

---

## `equation_parser()`

This will parse equations such as 10 * 10 which is passed in as an array with numbers and operands.

**Arguments**
- `equation (list)`
    - List of the ints and operands in order

**Returns**
- `value (int)`
    - The value of the equation 

This method work in a very simple manner and what it does is simply get the first integer and add it to a varibale called `total`. It then checks every even list item in `equation` argument which should be a arithmetics operator and if it is found then perform that arithmetic operation using the `total` and the integer after the arithmetic operator found.

---

## `concatenation_parser()`

This will parse concatenation of strings and variables with string values or integer values to concatenate arithmetics to strings together e.g. "Ryan " + last_name;

**Arguments**
- `concatenation_list (list)`
     - Array with all items needed seperated to perform concatenation

**Returns**
- `value (string)` 
    - Full string after concatenation done
- `error (list)` 
    - Return False with an error message in a list

This method will use the `concatenation_list` argument which is a list of token values that look like this `['"Ryan"', "+", "last_name"]`. It will loop through each of the list items and perform the concatenation by adding everything to a empty string in rder to form it. It is easy to differ from a string and a variable because a string will be surrounded in quotes whereas variable aren't.

      if item == 0:
          if current_value[0] == '"': 
              full_string += current_value[1:len(current_value) - 1]
          else: 
              full_string += self.get_variable_value(current_value)
          pass

Next, I simply check if every even number apart from 0 is a `+` to make sure the concatenation follows correct syntax and then if it is it will automatically add the next list item to the `full_string` variable. This step is repeated until the concatenation is complete and there are no more `+` operators. This is done with the following code:

    if item % 2 == 1:
        if current_value == "+": 
            # This checks if the value being checked is a string or a variable
            if concatenation_list[item + 1][0] != '"': 
                full_string += self.get_variable_value(concatenation_list[item + 1])
            else: 
                full_string += concatenation_list[item + 1][1:len(concatenation_list[item + 1]) - 1]
                        
        elif current_value == ",": 
            full_string += " " + concatenation_list[item + 1]

        else: 
          self.error_messages.append(["Error parsing equation, check that you are using correct operand",concatenation_list])
          
Finally, I just return the full string.

---

## `get_variable_value()`

This will get the value of a variable from the symbol tree and return the value if the variable exists or an error if it doesn't

**Arguments**
- `name (string)`
    - The name which we will search for in symbol tree

**Returns**
- `value (string)` 
    - The value of the variable if it is found
- `error (bool)`
    - Sends back False if it was not found

This method is simple as all it does is simply use the passed in argument `name` to loop through the `symbol_table` 2d array to see if it can find another variable with the same name and if it does will return `True` or `False` if it doesn't.

---

## `send_error_message()`

This will simply send all the found error messages within the source codeand return a list of error messages and tokens of which part of the source code caused that error.

**Arguments**
- `error_list (list)`
    - List with error message and tokens

This method will loop through each error message in the `error_message` global variable and print out every error with a descripttion along with the tokens which cause the error. It looks something like this:

    1. Variable `test` is not defined
    ['IDENTIFIER', 'print'] ['IDENTIFIER', 'test'] ['STATEMENT_END', ';']
    print test;
    
The error messages are stored as 2d arrays with every list item being a list with 2 list items which is first the description and then the tokens which make up the error, like such:

    [
    ['Variable `test` is not defined', ['IDENTIFIER', 'print'] ['IDENTIFIER', 'test'] ['STATEMENT_END', ';']],
    ...
    ]

---

## TODO `parse_for_loop`

---