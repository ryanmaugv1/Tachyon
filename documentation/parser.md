# **Parser**

> This documentation file for parser will soon be populated with clear pictures from notebook where all documentation has been done in detail with diagrams.

---

## Class Parser

The parser class will handle all the syntatic and symentic analysis of the the parsing for the code. It will also raise errors when syntax errors are found.

Class Variables, what they contain & why they are needed:

- `source_ast`

    This will initiall hold a dictionary with the key of `main_scope` with the value of an empty array where all the source code AST structures will be appended to. This will be used in order to be interpreted and compiled. The variable will look like this: `{'main_scope': []}`.

- `symbol_tree`

    This will be used in order to store variables with their name and value in the following format `['name', 'value']` so that I can perform semantical analysis and perform checks to see if a variable exists or not.

- `token_stream`

    This will hold the tokens that have just been produced by the lexical analyser which the parser will use to turn into an Abstract Syntax Tree (AST) and Symbol Trees so that syntatic and semantical analysis can be performed.