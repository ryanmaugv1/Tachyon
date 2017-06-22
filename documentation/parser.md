
# **Parser**

> ## **Class Parser**

The parser class will handle all the syntatic and symentic analysis of the the parsing for the code. It will also raise errors when syntax errors are found.

Class Variables, what they contain & why they are needed:

- `source_ast`

    This will initiall hold a dictionary with the key of `main_scope` with the value of an empty array where all the source code AST structures will be appended to. This will be used in order to be interpreted and compiled. The variable will look like this: `{'main_scope': []}`.

- `symbol_tree`

    This will be used in order to store variables with their name and value in the following format `['name', 'value']` so that I can perform semantical analysis and perform checks to see if a variable exists or not.

- `token_stream`

    This will hold the tokens that have just been produced by the lexical analyser which the parser will use to turn into an Abstract Syntax Tree (AST) and Symbol Trees so that syntatic and semantical analysis can be performed.

> ### **parse_if_statement()**


> ### **parse_variable_decleration()**

- **`Todo`**
    - Allow for more complex variable declerations like: `int ans = 12 + 1;` rather than simple one value variable declerations like this: `int ans = 13;`.
    - Modify symbol tree to add the variables scope too, so that a variable can only be called within the tachyon code if is within a specific scope.

> ### **parse_print()**



# Notes
    if str(type(literal_eval(item[1]))) == "<class " + "'" + ast[0]['VariableDeclerator'][0]['type'] + "'>":

    print("TypeError: Variable value does not conform to data type of " + str(type(literal_eval(item[1]))))
