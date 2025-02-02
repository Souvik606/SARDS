"""
Module: lexer

This module implements a simple lexical analyzer (lexer) for mathematical expressions.
It reads an input string and converts it into a sequence of tokens,
handling numbers, operators, and parentheses.

Classes:
- Token: Represents a single token with a type and an optional value.
- Lexer: Performs lexical analysis, converting input text into tokens.

Functions:
- run: Executes the lexer on a given input and returns tokens or errors.
"""

from Error_Class import *
from constants import *

class Token:
    """Represents a token in the input with a specific type and optional value."""

    def __init__(self, type_, value):
        """
        Initializes a Token instance.

        Parameters:
        - type_ (str): The type of the token (e.g., INT, FLOAT, PLUS).
        - value (any): The value of the token (e.g., a number for INT/FLOAT, or None for operators).
        """
        self.type = type_
        self.value = value

    def __repr__(self):
        """
        Returns a string representation of the token.

        Returns:
        - str: Formatted string representation of the token.
        """
        return f'{self.type}: {self.value}' if self.value is not None else f'{self.type}'

class Lexer:
    """Performs lexical analysis by reading input text and generating tokens."""

    def __init__(self, filename, text):
        """
        Initializes the Lexer with the input text.

        Parameters:
        - filename (str): The name of the source file being processed.
        - text (str): The input string to be tokenized.
        """
        self.filename = filename
        self.text = text
        self.pos = Position(-1, 0, -1, filename, text)  # Tracks position in the input text
        self.current_char = None  # Holds the current character being processed
        self.advance()

    def advance(self):
        """
        Moves to the next character in the input text.

        Updates the current character and position.
        """
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_number(self):
        """
        Extracts a numerical value (integer or float) from the input text.

        Returns:
        - Token: A token of type INT or FLOAT based on the extracted number.
        """
        number = ''
        is_float = False

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if is_float:  # Ensures only one decimal point in a float
                    break
                is_float = True
                number += '.'
            else:
                number += self.current_char
            self.advance()

        return Token(T_FLOAT, float(number)) if is_float else Token(T_INT, int(number))

    def enumerate_tokens(self):
        """
        Tokenizes the input text into a list of tokens.

        Returns:
        - list: A list of Token objects.
        - Error or None: Returns an error if an invalid character is encountered.
        """
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':  # Skips whitespace characters
                self.advance()
            elif self.current_char in DIGITS:  # Handles numbers
                tokens.append(self.make_number())
            elif self.current_char == '+':  # Addition operator
                tokens.append(Token(T_PLUS, None))
                self.advance()
            elif self.current_char == '-':  # Subtraction operator
                tokens.append(Token(T_MINUS, None))
                self.advance()
            elif self.current_char == '*':  # Multiplication operator
                tokens.append(Token(T_MUL, None))
                self.advance()
            elif self.current_char == '/':  # Division operator
                tokens.append(Token(T_DIVIDE, None))
                self.advance()
            elif self.current_char == '(':  # Left parenthesis
                tokens.append(Token(T_LPAREN, None))
                self.advance()
            elif self.current_char == ')':  # Right parenthesis
                tokens.append(Token(T_RPAREN, None))
                self.advance()
            else:
                # Handles illegal characters
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f'"{char}"')

        return tokens, None

def run(filename, text):
    """
    Executes the lexer on the given input text.

    Parameters:
    - filename (str): The name of the source file being processed.
    - text (str): The input string to be tokenized.

    Returns:
    - list: A list of tokens generated from the input.
    - Error or None: Returns an error if any invalid character is encountered.
    """
    lexer = Lexer(filename, text)
    tokens, errors = lexer.enumerate_tokens()
    return tokens, errors
