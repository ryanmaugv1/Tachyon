
# **Parser**

> ## **Class Parser**

The parser class will handle all the syntatic and symentic analysis of the the parsing for the code. It will also raise errors when syntax errors are found.

Class Variables, what they contain & why they are needed:

- `source_ast`

    This will initiall hold a dictionary with the key of `main_scope` with the value of an empty array where all the source code AST structures will be appended to. This will be used in order to be interpreted and compiled.

- `symbol_tree`

    This will be used in order to store variables in with their name and value in the follwoing format `['name', 'value']` so that I cam perform semanticl analysis and perform checks to see if a variable exists or not.

- `token_stream`

    This will hold the value of the tokens that have just been through the lexical analyser which the parser will use to turn the tokens into Abstract Syntax Tree (AST) and Symbol Trees so that syntatic and semantical analysis can be performed.

> ### parse_if_statement()


> ### parse_variable_decleration()


> ### parse_print()