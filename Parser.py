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
from variablesNode import *
from if_else_elif_statements import *
from for_loop import *


class ParseResult:
    """Stores the result of a parsing operation, including errors and the parsed node."""

    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        """Registers the result of a parsing operation, propagating errors and nodes."""
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        """Marks the parsing as successful and stores the resulting node."""
        self.node = node
        return self

    def failure(self, error):
        """Marks the parsing as failed and stores the associated error."""
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


class NumberNode:
    """Represents a numeric literal in the Abstract Syntax Tree (AST)."""

    def __init__(self, token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'


class UnaryOperationNode:
    """Represents a unary operation (e.g., negation) in the AST."""

    def __init__(self, operator, node):
        self.operator = operator
        self.node = node
        self.pos_start = self.operator.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'({self.operator}, {self.node})'


class BinaryOperationNode:
    """Represents a binary operation (e.g., addition, multiplication) in the AST."""

    def __init__(self, left_node, operator, right_node):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

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

    def peek(self):
        next_index = self.tok_index + 1
        if next_index < len(self.tokens):
            return self.tokens[next_index]
        return None

    def parse(self):
        """Initiates parsing and returns the final AST or an error if parsing fails."""
        if self.current_tok.type == T_KEYWORD and self.current_tok.value == 'define':
            result = self.statements()
        elif self.current_tok.type == T_IDENTIFIER:
            if self.peek() and self.peek().type == T_EQ:
                result = self.statements()
            else:
                result = self.expression()
        else:
            result = self.expression()

        if not result.error and self.current_tok.type != T_EOF:
            return result.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*', '/'"))
        return result

    def for_expression(self):
        res=ParseResult()
        step_value=None

        if not(self.current_tok.type==T_KEYWORD and self.current_tok.value=='Cycle'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'Cycle'"))

        res.register_advancement()
        self.advance()

        if not self.current_tok.type==T_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected identifier"))

        var_name=self.current_tok
        res.register_advancement()
        self.advance()

        if not self.current_tok.type==T_EQ:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected '='"))

        res.register_advancement()
        self.advance()

        start_value=res.register(self.expression())
        if res.error: return res

        if not self.current_tok.type==T_COLON:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected ':'"))

        res.register_advancement()
        self.advance()

        end_value=res.register(self.expression())
        if res.error:return res

        if self.current_tok.type==T_COLON:
            res.register_advancement()
            self.advance()

            step_value=res.register(self.expression())
            if res.error:return res

        if not self.current_tok.type==T_LPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected '{'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
            body_node = res.register(self.statements())
        else:
            body_node = res.register(self.expression())
        if res.error: return res

        if not self.current_tok.type == T_RPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

        res.register_advancement()
        self.advance()

        return res.success(ForNode(var_name,start_value,end_value,step_value,body_node))

    def if_expression(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not (self.current_tok.type == T_KEYWORD and self.current_tok.value == 'when'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected 'when'"))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error: return res

        if not self.current_tok.type == T_LPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
            expression = res.register(self.statements())
        else:
            expression = res.register(self.expression())

        if res.error: return res
        cases.append((condition, expression))

        if not self.current_tok.type == T_RPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

        res.register_advancement()
        self.advance()

        while self.current_tok and self.current_tok.type == T_KEYWORD and self.current_tok.value == 'orwhen':
            res.register_advancement()
            self.advance()

            condition = res.register(self.expression())
            if res.error: return res

            if not self.current_tok.type == T_LPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

            res.register_advancement()
            self.advance()

            if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
                expression = res.register(self.statements())
            else:
                expression = res.register(self.expression())

            if res.error: return res
            cases.append((condition, expression))

            if not self.current_tok.type == T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

        if self.current_tok and self.current_tok.type == T_KEYWORD and self.current_tok.value == 'otherwise':
            res.register_advancement()
            self.advance()

            if not self.current_tok.type == T_LPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

            res.register_advancement()
            self.advance()

            if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
                expression = res.register(self.statements())
            else:
                expression = res.register(self.expression())
            if res.error: return res
            else_case = expression

            if not self.current_tok.type == T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

        return res.success(IfNode(cases, else_case))

    def factor(self):
        """Parses factors (numbers, parentheses, and unary operations)."""
        res = ParseResult()
        token = self.current_tok

        if token.type in (T_PLUS, T_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOperationNode(token, factor))

        elif token.type in (T_INT, T_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))

        elif token.type == T_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VariableUseNode(token))

        elif token.type == T_LPAREN:
            res.register_advancement()
            self.advance()
            expression = res.register(self.expression())
            if res.error:
                return res
            if self.current_tok.type == T_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expression)
            else:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))

        elif token.type == T_KEYWORD and token.value == 'when':
            if_expr = res.register(self.if_expression())
            if res.error: return res
            return res.success(if_expr)

        elif token.type == T_KEYWORD and token.value == 'Cycle':
            for_expr = res.register(self.for_expression())
            if res.error: return res
            return res.success(for_expr)

        return res.failure(
            InvalidSyntaxError(token.pos_start, token.pos_end, "Expected int, float,identifier,'+','-'or '('"))

    def term(self):
        """Parses terms, handling multiplication and division operations."""
        res = ParseResult()
        left_node = res.register(self.factor())
        if res.error:
            return res

        while self.current_tok and self.current_tok.type in (T_MUL, T_DIVIDE):
            operator = self.current_tok
            res.register_advancement()
            self.advance()
            right_node = res.register(self.factor())
            if res.error:
                return res
            left_node = BinaryOperationNode(left_node, operator, right_node)

        return res.success(left_node)

    def statements(self):
        res = ParseResult()

        if self.current_tok.type == T_KEYWORD and self.current_tok.value == 'define':
            res.register_advancement()
            self.advance()

            if self.current_tok.type != T_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != T_EQ:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))

            res.register_advancement()
            self.advance()

            expression = res.register(self.expression())
            if res.error: return res
            return res.success(VariableAssignNode(var_name, expression))

        elif self.current_tok.type == T_IDENTIFIER:
            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != T_EQ:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ="))

            res.register_advancement()
            self.advance()

            expression = res.register(self.expression())
            if res.error: return res

            return res.success(VariableAssignNode(var_name, expression))

        return res.failure(
            InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'define' or identifier"))

    def expression(self):
        res = ParseResult()

        left_node = res.register(self.comp_expression())
        if res.error: return res

        while self.current_tok and self.current_tok.type == T_KEYWORD and self.current_tok.value in ('and', 'or'):
            operator = self.current_tok
            res.register_advancement()
            self.advance()

            right_node = res.register(self.comp_expression())
            if res.error: return res

            left_node = BinaryOperationNode(left_node, operator, right_node)

        node = res.register(res.success(left_node))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected int,float,identifier"))
        return res.success(node)

    def comp_expression(self):
        res = ParseResult()

        if self.current_tok.type == T_KEYWORD and self.current_tok.value == 'not':
            operator_token = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expression())
            if res.error: return res
            return res.success(UnaryOperationNode(operator_token, node))

        left_node = res.register(self.arith_expression())
        if res.error: return res

        while self.current_tok and self.current_tok.type in (T_EE, T_LT, T_GT, T_GTE, T_LTE):
            operator = self.current_tok
            res.register_advancement()
            self.advance()
            right_node = res.register(self.arith_expression())
            if res.error: return res
            left_node = BinaryOperationNode(left_node, operator, right_node)

        node = res.register(res.success(left_node))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected int,float,identifier,'+','-','not' or '('"))
        return res.success(node)

    def arith_expression(self):
        """Parses full expressions, handling addition and subtraction operations."""
        res = ParseResult()
        left_node = res.register(self.term())
        if res.error:
            return res

        while self.current_tok and self.current_tok.type in (T_PLUS, T_MINUS):
            operator = self.current_tok
            res.register_advancement()
            self.advance()
            right_node = res.register(self.term())
            if res.error:
                return res
            left_node = BinaryOperationNode(left_node, operator, right_node)

        node = res.register(res.success(left_node))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected 'define',int,float,identifier,'+','-' or '('"))
        return res.success(node)
