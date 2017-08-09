# How to Contribute
This document will detail how to get started with contributing to this project.

## Setting up environment
In order to set up your development envornment just follow these few steps and you will be set to go and start contributing.

> Before beginning you should know how the project is structured and works when the `./src/main.py` file is executed.

When the `./src/main.py` file is executed the Tachyon source code which we are testing on and is located in `./test.txt` file. It will be run through the `lexer.py` and the outputs from that will be passed on to the `parser.py` file. It will do this sequentially everytime you execute the programme.

1. Clone this repo by either downloading the zip from the repo or cloning it from your terminal using this command `https://github.com/RyanMaugin/Tachyon.git`
2. You then want to navigate inside the repo after cloning it `cd Tachyon`.
3. Now that you are inside the project you can run it using the command `python3 ./src/main.py`.
4. If you want to run tests you can run the files inside the `tests` directory which will have a pname pattern of `{module_name}_tests.py`.

## What you can contribute to

Any optimisation are welcomed as contributions that will help the programme be more efficient. Overall all contributions are welcomed as long as it betters or refines what already exists.

## Guideline for each contribution

When making contributions the guidelines are to:

- [ ] Add comments since this is a toy language it is meant for people to understand and learn from.
- [ ] Keep code as efficient and minimal as possible when you can.
- [ ] Make sure that code is in the right place such as the right class or file.

# Roadmap

- **Lexer**
- **Parser**
  - **Variable Decleration**
  - **Concatenation**
  - **Arithmetics**
  - **Conditional Statements**
  - **Built-in function calling**
- **Optimisation**
- **Code Generation** `<-- current`
- CG Optimsation
- Adding new features to language

# How to get in touch
Haven any questions?

You can email me @ ryan.maugin@adacollege.org.uk
