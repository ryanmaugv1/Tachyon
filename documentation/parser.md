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

---

## `parse_built_in_function()`

This will parse built in methods and their parameters to form an AST.

**Arguments**
- `token_stream (list)` 
    - The token stream starting from where the builtin function was found
- `isInBody (bool)`
    - This will hold True if this function is being run from body parsing

---

## `variable_decleration_parsing()`

This method will parse variable declerations and add them to the source AST or return them if variable decleration is being parsed for body of a statement.

**Arguments**
- `token_stream (list)`
    - The token stream starting from where the variable decleration was found

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
    - The condition of the body being parsed
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