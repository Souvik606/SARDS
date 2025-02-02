"""
Module: parser

This module implements a recursive descent parser for mathematical expressions.
It converts a sequence of tokens into an Abstract Syntax Tree (AST) by following
rules for arithmetic expressions, including handling unary and binary operations.

Classes:
- ParseResult: Stores the result of a parsing operation, including success or failure.
- NumberNode: Represents a numeric literal in the AST.
- UnaryOperationNode: Represents a unary operation (e.g., negation) in the AST.
- BinaryOperationNode: Represents a binary operation (e.g., addition, multiplication) in the AST.
- Parser: Performs parsing by analyzing token sequences and constructing an AST.

Methods:
- ParseResult:
  - register(res): Handles the propagation of errors and nodes during parsing.
  - success(node): Marks parsing as successful with a resulting node.
  - failure(error): Marks parsing as failed with an error.

- Parser:
  - advance(): Moves to the next token in the sequence.
  - parse(): Initiates parsing and returns the final AST or an error.
  - factor(): Parses factors (numbers, parentheses, unary operations).
  - term(): Parses terms (handles multiplication and division operations).
  - expression(): Parses full expressions (handles addition and subtraction operations).
"""

from Error_Class import *
from constants import *

class ParseResult:
    """Stores the result of a parsing operation, including errors and the parsed node."""
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        """Registers the result of a parsing operation, propagating errors and nodes."""
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        """Marks the parsing as successful and stores the resulting node."""
        self.node = node
        return self

    def failure(self, error):
        """Marks the parsing as failed and stores the associated error."""
        self.error = error
        return self

class NumberNode:
    """Represents a numeric literal in the Abstract Syntax Tree (AST)."""
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'

class UnaryOperationNode:
    """Represents a unary operation (e.g., negation) in the AST."""
    def __init__(self, operator, node):
        self.operator = operator
        self.node = node

    def __repr__(self):
        return f'({self.operator}, {self.node})'

class BinaryOperationNode:
    """Represents a binary operation (e.g., addition, multiplication) in the AST."""
    def __init__(self, left_node, operator, right_node):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operator}, {self.right_node})'

class Parser:
    """Performs recursive descent parsing of tokenized mathematical expressions."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_tok = None
        self.tok_index = -1
        self.advance()

    def advance(self):
        """Moves to the next token in the token sequence."""
        self.tok_index += 1
        if self.tok_index < len(self.tokens):
            self.current_tok = self.tokens[self.tok_index]
        else:
            self.current_tok = None

    def parse(self):
        """Initiates parsing and returns the final AST or an error if parsing fails."""
        result = self.expression()
        if not result.error and self.current_tok.type != T_EOF:
            return result.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*', '/'"))
        return result

    def factor(self):
        """Parses factors (numbers, parentheses, and unary operations)."""
        res = ParseResult()
        token = self.current_tok

        if token.type in (T_PLUS, T_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOperationNode(token, factor))

        elif token.type in (T_INT, T_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(token))

        elif token.type == T_LPAREN:
            res.register(self.advance())
            expression = res.register(self.expression())
            if res.error:
                return res
            if self.current_tok.type == T_RPAREN:
                res.register(self.advance())
                return res.success(expression)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))

        return res.failure(InvalidSyntaxError(token.pos_start, token.pos_end, "Expected int or float"))

    def term(self):
        """Parses terms, handling multiplication and division operations."""
        res = ParseResult()
        left_node = res.register(self.factor())
        if res.error:
            return res

        while self.current_tok and self.current_tok.type in (T_MUL, T_DIVIDE):
            operator = self.current_tok
            res.register(self.advance())
            right_node = res.register(self.factor())
            if res.error:
                return res
            left_node = BinaryOperationNode(left_node, operator, right_node)

        return res.success(left_node)

    def expression(self):
        """Parses full expressions, handling addition and subtraction operations."""
        res = ParseResult()
        left_node = res.register(self.term())
        if res.error:
            return res

        while self.current_tok and self.current_tok.type in (T_PLUS, T_MINUS):
            operator = self.current_tok
            res.register(self.advance())
            right_node = res.register(self.term())
            if res.error:
                return res
            left_node = BinaryOperationNode(left_node, operator, right_node)

        return res.success(left_node)
