"""
Module: token_definitions

This module defines constants used for tokenization, including digit characters 
and token types for mathematical expressions.
"""
import string

# Set of characters representing numerical digits
DIGITS = '0123456789'
LETTERS=string.ascii_letters
LETTERS_DIGITS=DIGITS+LETTERS

# Token Types for mathematical operations and symbols
T_INT = 'INT'         # Integer number token
T_FLOAT = 'FLOAT'     # Floating-point number token
T_IDENTIFIER='IDENTIFIER'#Identifier token
T_KEYWORD='KEYWORD'
T_PLUS = 'PLUS'      # Addition operator (+)
T_MINUS = 'MINUS'    # Subtraction operator (-)
T_MUL = 'MUL'        # Multiplication operator (*)
T_DIVIDE = 'DIV'
T_EQ='EQUAL'# Division operator (/)
T_LPAREN = 'LPAREN'  # Left parenthesis (
T_RPAREN = 'RPAREN'  # Right parenthesis )
T_EOF='EOF'          # End of File

#Keywords list

KEYWORDS=['define']
