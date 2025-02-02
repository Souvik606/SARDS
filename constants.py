"""
Module: token_definitions

This module defines constants used for tokenization, including digit characters 
and token types for mathematical expressions.
"""

# Set of characters representing numerical digits
DIGITS = '0123456789'

# Token Types for mathematical operations and symbols
T_INT = 'INT'         # Integer number token
T_FLOAT = 'FLOAT'     # Floating-point number token
T_PLUS = 'PLUS'      # Addition operator (+)
T_MINUS = 'MINUS'    # Subtraction operator (-)
T_MUL = 'MUL'        # Multiplication operator (*)
T_DIVIDE = 'DIV'     # Division operator (/)
T_LPAREN = 'LPAREN'  # Left parenthesis (
T_RPAREN = 'RPAREN'  # Right parenthesis )
