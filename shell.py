"""
Module: main

This module serves as the entry point for executing the lexer and parser.
It provides an interactive Read-Eval-Print Loop (REPL) where users can input
mathematical expressions, which are then tokenized, parsed, and displayed
as an Abstract Syntax Tree (AST).

## Overview:
1. **Lexical Analysis (Lexer)**:
   - Converts the input text into a sequence of tokens.
   - Identifies numbers, operators, and parentheses.
   - Returns a list of tokens or an error if invalid characters are found.

2. **Parsing (Parser)**:
   - Converts the tokenized input into a structured AST.
   - Follows defined grammar rules for mathematical expressions.
   - Returns a valid AST or a syntax error.

3. **Interactive Execution (REPL)**:
   - Repeatedly asks for user input.
   - Displays either the parsed AST or an error message.

"""

from Lexer import *  # Importing the lexer module for tokenization
from Parser import * # Importing the parser module for syntax analysis
from Interpreter import *


def run(filename, text):
    """
    Executes the lexer and parser on the given input expression.

    This function first tokenizes the input text using the Lexer. If successful,
    the token list is passed to the Parser, which constructs an Abstract Syntax Tree (AST).
    Any errors encountered during tokenization or parsing are returned.

    Parameters:
    - filename (str): The name of the source file (used for error reporting).
    - text (str): The mathematical expression to be analyzed.

    Returns:
    - tuple:
        - AST (Abstract Syntax Tree): The parsed representation of the expression.
        - Error (if any): Provides details of any encountered errors.

    Example Usage:
    --------------
    ast, error = run('<stdin>', '3 + 4 * (2 - 1)')
    if error:
        print(error.to_string())
    else:
        print(ast)
    """
    lexer = Lexer(filename, text)  # Initialize the Lexer with the input text
    tokens, error = lexer.enumerate_tokens()  # Generate tokens

    # If lexical analysis encounters an error, return it
    if error:
        return None, error

    # Pass the tokens to the parser
    parser = Parser(tokens)
    syntax_tree = parser.parse()  # Generate AST

    # Return the parsed AST and any errors encountered
    if syntax_tree.error:
        return None,syntax_tree.error

    interpreter=Interpreter()
    context=Context('<program>')
    result=interpreter.visit(syntax_tree.node,context)

    return result.value, result.error


# REPL (Read-Eval-Print Loop) for continuous user interaction
while True:
    text = input('code > ')  # Prompt user for an expression
    result, errors = run('<stdin>', text)  # Process input

    # Print errors if encountered, otherwise display the AST
    if errors:
        print(errors.to_string())
    else:
        print(result)
