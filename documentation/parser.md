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

- The Prebuilt function type which is basically the name of the function e.g `print "Ryan";` the type will be `print` and this token has to be at token index 1.

      if token == 0:
          ast['PrebuiltFunction'].append( {'type': token_stream[token][1]} )

- At token index 2 I look for the parameter that is being passed in which has to be either a value like `string`, `int` or `bool` etc. Inside this check I also perform various operations lie getting the value of a variable if the the value passed is an `IDENTIFIER` (var) type.

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

**Returns**

- `ast (dict)`
    - The condtion ast without the body
- `tokens_checked (int)`
    - The count of tokens checked that made up the condition statement

---

## `conditional_statement_parser()`

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

---

## `get_statement_body()`

This will get the tokens that make up the body of a statement and return the tokens.

**Arguments**
- `token_stream (list)`
    - This will hold the tokens after the scope definer

**Returns**
- `tokens_list (list)`
    - Returns tokens that make up the body for statement

---

## `perform_conditional_checks()`

This will perform the condtitional checks and see whether the condition evaluates to true or false.

**Arguments**
- `comparison_type (str)`
    - The comparison operator e.g ==, < or >=
- `values (list)`
    - The values that comparison will be applied on
- `token_checked (int)`
    - For displaying the error messages tokens

**Returns**
- `boolean`
    - True or False based on condition evaluation

---

## `equation_parser()`

This will parse equations such as 10 * 10 which is passed in as an array with numbers and operands.

**Arguments**
- `equation (list)`
    - List of the ints and operands in order

**Returns**
- `value (int)`
    - The value of the equation 

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

---

## `send_error_message()`

This will simply send all the found error messages within the source codeand return a list of error messages and tokens of which part of the source code caused that error.

**Arguments**
- `error_list (list)`
    - List with error message and tokens

---
