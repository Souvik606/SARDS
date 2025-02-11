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

from core.error import *
from core.constants import *
from ast_nodes.for_node import *
from ast_nodes.if_node import *
from ast_nodes.jump_node import *
from data_types.list_type import ListNode
from data_types.string_type import *
from ast_nodes.functions_node import *
from ast_nodes.variables_node import *
from ast_nodes.while_node import *
from ast_nodes.switch_node import *

class ParseResult:
    """Stores the result of a parsing operation, including errors and the parsed node."""

    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        """Registers the result of a parsing operation, propagating errors and nodes."""
        self.last_registered_advance_count = res.advance_count
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

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)


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


class TernaryOperationNode:
    """Represents a ternary operation ( e.g. a>b ? show(a) : show(b) )"""

    def __init__(self, comp_node, true_node, false_node):
        self.comp_node = comp_node
        self.true_node = true_node
        self.false_node = false_node
        self.pos_start = self.comp_node.pos_start
        self.pos_end = self.false_node.pos_end

    def __repr__(self):
        return f'({self.comp_node} ? {self.true_node} : {self.false_node})'


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
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_index -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.tok_index >= 0 and self.tok_index < len(self.tokens):
            self.current_tok = self.tokens[self.tok_index]

    def peek(self):
        next_index = self.tok_index + 1
        if next_index < len(self.tokens):
            return self.tokens[next_index]
        return None

    def parse(self):
        """Initiates parsing and returns the final AST or an error if parsing fails."""
        result = self.multiline()

        if not result.error and self.current_tok.type != T_EOF:
            print(self.current_tok)
            return result.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*', '/'"))
        return result

    def multiline(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == T_NEWLINE:
            res.register_advancement()
            self.advance()

        if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
            statement = res.register(self.statements())

        else:
            statement = res.register(self.expression())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_tok.type == T_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements: break

            if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
                statement = res.try_register(self.statements())

            else:
                statement = res.try_register(self.expression())

            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(statements, pos_start, self.current_tok.pos_end.copy()))

    def list_expression(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != T_LPAREN3:
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected '['"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_RPAREN3:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expression()))
            if res.error: return res
            while self.current_tok and self.current_tok.type == T_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expression()))
                if res.error: return res

            if self.current_tok.type != T_RPAREN3:
                print(self.current_tok)
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected ',' or ']"))

            res.register_advancement()
            self.advance()

        return res.success(ListNode(element_nodes, pos_start, self.current_tok.pos_end.copy()))

    def function_definition(self):
        res = ParseResult()

        if not (self.current_tok.type == T_KEYWORD and self.current_tok.value == 'method'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'method'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != T_LPAREN:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '('"))
        else:
            var_name_tok = None
            if self.current_tok.type != T_LPAREN:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '('"))

        res.register_advancement()
        self.advance()

        arg_name_toks = []

        if self.current_tok.type == T_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok and self.current_tok.type == T_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != T_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != T_RPAREN:
                print(self.current_tok)
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ',' or ')'"))

        else:
            if self.current_tok.type != T_RPAREN:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                       "Expected identifier  or ')'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != T_LPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.multiline())
            if res.error: return res

            if not self.current_tok.type == T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

            return res.success(FunctionDefinitionNode(var_name_tok, arg_name_toks, body, True))

        if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
            body_node = res.register(self.statements())
        else:
            body_node = res.register(self.expression())
        if res.error: return res

        if self.current_tok.type != T_RPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

        res.register_advancement()
        self.advance()

        return res.success(FunctionDefinitionNode(var_name_tok, arg_name_toks, body_node, False))

    def function_call(self):
        res = ParseResult()
        arg_nodes = []

        if self.current_tok.type == T_IDENTIFIER:
            call_node = res.register(res.success(VariableUseNode(self.current_tok)))
            res.register_advancement()
            self.advance()
        else:
            res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))

        if res.error:
            return res

        if self.current_tok.type != T_LPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '('"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_RPAREN:
            res.register_advancement()
            self.advance()
        else:
            arg_nodes.append(res.register(self.expression()))
            if res.error: return res

            while self.current_tok and self.current_tok.type == T_COMMA:
                res.register_advancement()
                self.advance()

                arg_nodes.append(res.register(self.expression()))
                if res.error: return res

            if self.current_tok.type != T_RPAREN:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected ',' or ')"))

            res.register_advancement()
            self.advance()

        return res.success(FunctionCallNode(call_node, arg_nodes))

    def switch_statement(self):
        res = ParseResult()
        cases = []
        if not (self.current_tok.type == T_KEYWORD and self.current_tok.value == 'menu'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'menu'"))

        res.register_advancement()
        self.advance()

        selection = res.register(self.ternary_expression())
        if res.error: return res

        if not self.current_tok.type == T_LPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

        res.register_advancement()
        self.advance()

        while self.current_tok.type == T_NEWLINE:
            res.register_advancement()
            self.advance()

        found_default = False
        count = 0
        
        while(self.current_tok.type == T_KEYWORD and (self.current_tok.value == 'choice' or self.current_tok.value == 'fallback')):
            if(self.current_tok.type == T_KEYWORD and self.current_tok.value == 'choice'):
                case = res.register(self.case_statement())
                if res.error: return res
                cases.append(case)
                while self.current_tok.type == T_NEWLINE:
                    res.register_advancement()
                    self.advance()
            else:
                if found_default == True:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Multiple 'fallback' statements found"))
                found_default = True
                case = res.register(self.default_statement())
                if res.error: return res
                cases.append(case)
                while self.current_tok.type == T_NEWLINE:
                    res.register_advancement()
                    self.advance()
            count = count + 1
            
        if count == 0:
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'choice' or 'fallback'"))
            
        if not self.current_tok.type == T_RPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

        res.register_advancement()
        self.advance()

        return res.success(SwitchNode(selection, cases, False))

    def case_statement(self):
        res = ParseResult()
        case = None

        if not (self.current_tok.type == T_KEYWORD and self.current_tok.value == 'choice'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'choice'"))
        res.register_advancement()
        self.advance()

        choice_val = res.register(self.ternary_expression())
        if res.error: return res

        if not self.current_tok.type == T_LPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.multiline())
            if res.error: return res
            case = (choice_val, body, True)
            if not self.current_tok.type == T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()
        else:
            if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
                body_node = res.register(self.statements())
            else:
                body_node = res.register(self.expression())
            if res.error: return res
            case = (choice_val, body_node, False)
            if not self.current_tok.type == T_RPAREN2:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

        return res.success(case)

    def default_statement(self):
        res = ParseResult()
        default_case = None

        if not (self.current_tok.type == T_KEYWORD and self.current_tok.value == 'fallback'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'fallback'"))
        res.register_advancement()
        self.advance()

        if not self.current_tok.type == T_LPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.multiline())
            if res.error: return res
            default_case = (None, body, True)
            if not self.current_tok.type == T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()
        else:
            if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
                body_node = res.register(self.statements())
            else:
                body_node = res.register(self.expression())
            if res.error: return res
            default_case = (None, body_node, False)
            if not self.current_tok.type == T_RPAREN2:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

        return res.success(default_case)

    def while_expression(self):
        res = ParseResult()

        if not (self.current_tok.type == T_KEYWORD and self.current_tok.value == 'whenever'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'whenever'"))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error: return res

        if not self.current_tok.type == T_LPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.multiline())
            if res.error: return res

            if not self.current_tok.type == T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
            body_node = res.register(self.statements())
        else:
            body_node = res.register(self.expression())
        if res.error: return res

        if not self.current_tok.type == T_RPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

        res.register_advancement()
        self.advance()

        return res.success(WhileNode(condition, body_node, False))

    def for_expression(self):
        res = ParseResult()
        step_value = None

        if not (self.current_tok.type == T_KEYWORD and self.current_tok.value == 'Cycle'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'Cycle'"))

        res.register_advancement()
        self.advance()

        if not self.current_tok.type == T_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if not self.current_tok.type == T_EQ:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expression())
        if res.error: return res

        if not self.current_tok.type == T_COLON:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ':'"))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expression())
        if res.error: return res

        if self.current_tok.type == T_COLON:
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expression())
            if res.error: return res

        if not self.current_tok.type == T_LPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == T_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.multiline())
            if res.error: return res

            if not self.current_tok.type == T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
            body_node = res.register(self.statements())
        else:
            body_node = res.register(self.expression())
        if res.error: return res

        if not self.current_tok.type == T_RPAREN2:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

        res.register_advancement()
        self.advance()

        return res.success(ForNode(var_name, start_value, end_value, step_value, body_node, False))

    def if_expression(self):
        res = ParseResult()
        cases = []

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

        if self.current_tok.type == T_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.multiline())
            if res.error: return res
            print(statements)
            cases.append((condition, statements, True))

            if self.current_tok.type != T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

            all_cases = res.register(self.elif_or_else_expression())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        else:
            if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
                expression = res.register(self.statements())
            else:
                expression = res.register(self.expression())
            if res.error: return res
            cases.append((condition, expression, False))

            if self.current_tok.type != T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

            all_cases = res.register(self.elif_or_else_expression())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success(IfNode(cases, else_case))

    def elif_or_else_expression(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.type == T_KEYWORD and self.current_tok.value == 'orwhen':
            all_cases = res.register(self.elif_expression())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.else_expression())
            if res.error: return res

        return res.success((cases, else_case))

    def elif_expression(self):
        res = ParseResult()
        cases = []

        if not (self.current_tok.type == T_KEYWORD and self.current_tok.value == 'orwhen'):
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

        if self.current_tok.type == T_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.multiline())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.current_tok.type != T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

            all_cases = res.register(self.elif_or_else_expression())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        else:
            if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
                expression = res.register(self.statements())
            else:
                expression = res.register(self.expression())
            if res.error: return res
            cases.append((condition, expression, False))

            if self.current_tok.type != T_RPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

            res.register_advancement()
            self.advance()

            all_cases = res.register(self.elif_or_else_expression())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def else_expression(self):
        res = ParseResult()
        else_case = None

        if self.current_tok.type == T_KEYWORD and self.current_tok.value == 'otherwise':
            res.register_advancement()
            self.advance()

            if not self.current_tok.type == T_LPAREN2:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))

            res.register_advancement()
            self.advance()

            if self.current_tok.type == T_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.multiline())
                if res.error: return res
                else_case = (statements, True)

                if not self.current_tok.type == T_RPAREN2:
                    return res.failure(
                        InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

                res.register_advancement()
                self.advance()

            else:
                if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
                    expression = res.register(self.statements())
                else:
                    expression = res.register(self.expression())
                if res.error: return res

                if not self.current_tok.type == T_RPAREN2:
                    return res.failure(
                        InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))

                res.register_advancement()
                self.advance()

                else_case = (expression, False)

        return res.success(else_case)

    def unary(self):
        res = ParseResult()
        token = self.current_tok

        if token.type in (T_PLUS, T_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.unary())
            if res.error:
                return res
            return res.success(UnaryOperationNode(token, factor))

        return self.exponent()

    def exponent(self):
        res = ParseResult()
        left_node = res.register(self.factor())
        if res.error:
            return res
        while self.current_tok and self.current_tok.type == T_EXP:
            operator = self.current_tok
            res.register_advancement()
            self.advance()
            right_node = res.register(self.unary())
            if res.error:
                return res
            left_node = BinaryOperationNode(left_node, operator, right_node)

        node = res.register(res.success(left_node))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected 'define',int,float,identifier,'+','-' or '('"))
        return res.success(node)

    def ternary_expression(self):
        res = ParseResult()
        if self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_EQ:
            comp_node = res.register(self.statements())
        else:
            comp_node = res.register(self.logical_expression())
        if res.error:
            return res
        false_node = true_node = None

        while self.current_tok and self.current_tok.type == T_QUESTION:
            res.register_advancement()
            self.advance()
            true_node = res.register(self.ternary_expression())
            if res.error:
                return res
            if self.current_tok and not self.current_tok.type == T_COLON:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ':' "))

            res.register_advancement()
            self.advance()
            false_node = res.register(self.ternary_expression())
            if res.error:
                return res

        if not (true_node and false_node): return res.success(comp_node)

        return res.success(TernaryOperationNode(comp_node, true_node, false_node))

    def factor(self):
        """Parses factors (numbers, parentheses, and unary operations)."""
        res = ParseResult()
        token = self.current_tok

        if token.type in (T_INT, T_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))

        elif token.type == T_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(token))

        elif self.current_tok and self.current_tok.type == T_IDENTIFIER and self.peek() and self.peek().type == T_LPAREN:
            call_expression = res.register(self.function_call())
            if res.error: return res
            return res.success(call_expression)

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

        elif token.type == T_KEYWORD and token.value == 'whenever':
            while_expr = res.register(self.while_expression())
            if res.error: return res
            return res.success(while_expr)

        elif token.type == T_KEYWORD and token.value == 'method':
            method_expr = res.register(self.function_definition())
            if res.error: return res
            return res.success(method_expr)
        
        elif token.type == T_KEYWORD and token.value == 'menu':
            switch_statement = res.register(self.switch_statement())
            if res.error: return res
            return res.success(switch_statement)

        elif token.type == T_LPAREN3:
            list_expression = res.register(self.list_expression())
            if res.error: return res
            return res.success(list_expression)

        return res.failure(
            InvalidSyntaxError(token.pos_start, token.pos_end, "Expected int, float,identifier,'+','-'or '('"))

    def term(self):
        """Parses terms, handling multiplication and division operations."""
        res = ParseResult()

        left_node = res.register(self.unary())
        if res.error:
            return res

        while self.current_tok and self.current_tok.type in (T_MUL, T_DIVIDE, T_MODULUS, T_FLOOR):
            operator = self.current_tok
            res.register_advancement()
            self.advance()
            right_node = res.register(self.unary())
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

        if self.current_tok.type == T_KEYWORD and self.current_tok.value == 'yield':
            res.register_advancement()
            self.advance()

            expression = res.try_register(self.expression())
            if not expression:
                self.reverse(res.to_reverse_count)
            return res.success(
                ReturnNode(expression, self.current_tok.pos_start.copy(), self.current_tok.pos_start.copy()))

        elif self.current_tok.type == T_KEYWORD and self.current_tok.value == 'proceed':
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(self.current_tok.pos_start.copy(), self.current_tok.pos_start.copy()))

        elif self.current_tok.type == T_KEYWORD and self.current_tok.value == 'escape':
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(self.current_tok.pos_start.copy(), self.current_tok.pos_start.copy()))
        else:
            ternary_node = res.register(self.ternary_expression())
            if res.error: return res
            node = res.register(res.success(ternary_node))
            if res.error:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                      "Expected int,float,identifier"))
            return res.success(node)

    def logical_expression(self):

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
