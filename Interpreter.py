"""
interpreter.py

This module defines the components needed for interpreting an abstract syntax tree (AST).
It includes classes for handling runtime context, execution results, and evaluating expressions.

Classes:
- Context: Maintains execution context (e.g., scope, parent context).
- RunTimeResult: Stores the result of an evaluation, including errors.
- Interpreter: Evaluates AST nodes and executes operations.
"""

from NumberDataType import *
from constants import *
from list_data_type import *


class Context:
    """
    Represents the execution context of a program.

    Attributes:
    - display_name (str): The name of the current execution context.
    - parent (Context, optional): The parent context (e.g., caller function).
    - parent_entry_pos (optional): The position in the parent where this context was entered.
    """

    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        """
        Initializes a new execution context.

        Parameters:
        - display_name (str): The name of the execution context.
        - parent (Context, optional): The parent execution context.
        - parent_entry_pos (optional): The entry position in the parent context.
        """
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


class RunTimeResult:
    """
    Represents the result of evaluating an AST node.

    Attributes:
    - value (any): The computed value.
    - error (Exception, optional): The error encountered, if any.
    """

    def __init__(self):
        """
        Initializes a new runtime result instance.
        """
        self.value = None
        self.error = None

    def register(self, res):
        """
        Registers the result of an evaluation.

        If an error is encountered, it is stored and execution halts.

        Parameters:
        - res (RunTimeResult): The result to register.

        Returns:
        - The computed value if no error occurred.
        """
        if res.error:
            self.error = res.error  # Fixed incorrect assignment (previously `error`)
        return res.value

    def success(self, value):
        """
        Marks the result as a success.

        Parameters:
        - value (any): The computed value.

        Returns:
        - self: The current instance with updated value.
        """
        self.value = value
        return self

    def failure(self, error):
        """
        Marks the result as a failure.

        Parameters:
        - error (Exception): The encountered error.

        Returns:
        - self: The current instance with updated error.
        """
        self.error = error
        return self


class Interpreter:
    """
    Interprets an abstract syntax tree (AST) by visiting its nodes and evaluating expressions.

    Methods:
    - visit(node, context): Determines the appropriate visit method for a node.
    - visit_NumberNode(node, context): Evaluates a number node.
    - visit_BinaryOperationNode(node, context): Evaluates binary operations (+, -, *, /).
    - visit_UnaryOperationNode(node, context): Evaluates unary operations (-).
    """

    def visit(self, node, context):
        """
        Visits an AST node and executes the corresponding evaluation method.

        Parameters:
        - node (AST Node): The node to visit.
        - context (Context): The execution context.

        Returns:
        - RunTimeResult: The evaluation result.
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        """
        Handles cases where no visit method is defined for a node type.

        Parameters:
        - node (AST Node): The unrecognized node.
        - context (Context): The execution context.

        Raises:
        - Exception: Indicates that the node type is unsupported.
        """
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_ListNode(self, node, context):
        res = RunTimeResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error: return res

        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_StringNode(self, node, context):
        return RunTimeResult().success(
            String(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_FunctionDefinitionNode(self, node, context):
        from FunctionType import Function
        res = RunTimeResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.return_null).set_context(context).set_pos(
            node.pos_start,
            node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_FunctionCallNode(self, node, context):
        res = RunTimeResult()
        args = []

        call_value = res.register(self.visit(node.call_node, context))
        if res.error: return res
        call_value = call_value.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return_value = res.register(call_value.execute(args))
        if res.error: return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)

        return res.success(return_value)

    def visit_WhileNode(self, node, context):
        res = RunTimeResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error: return res

            if not condition.value: break

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res

        return res.success(
            Number(0) if node.return_null else List(elements).set_context(context).set_pos(node.pos_start,
                                                                                           node.pos_end))

    def visit_ForNode(self, node, context):
        res = RunTimeResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error: return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error: return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error: return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i <= end_value.value
        else:
            condition = lambda: i >= end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res

        return res.success(
            Number(0) if node.return_null else List(elements).set_context(context).set_pos(node.pos_start,
                                                                                           node.pos_end))

    def visit_IfNode(self, node, context):
        res = RunTimeResult()

        for condition, expression, return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.value != 0:
                expression_value = res.register(self.visit(expression, context))
                if res.error: return res
                return res.success(Number(0) if return_null else expression_value)

        if node.else_case:
            expression,return_null=node.else_case
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(Number(0) if return_null else else_value)

        return res.success(Number(0))

    def visit_VariableUseNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if value is None:
            return res.failure(RuntimeError(node.pos_start, node.pos_end, f"'{var_name}' is not defined", context))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VariableAssignNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))

        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_NumberNode(self, node, context):
        """
        Evaluates a number node.

        Parameters:
        - node (NumberNode): The number node to evaluate.
        - context (Context): The execution context.

        Returns:
        - RunTimeResult: The evaluation result containing a Number instance.
        """
        return RunTimeResult().success(
            Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinaryOperationNode(self, node, context):
        """
        Evaluates a binary operation node (e.g., addition, subtraction).

        Parameters:
        - node (BinaryOperationNode): The binary operation node.
        - context (Context): The execution context.

        Returns:
        - RunTimeResult: The evaluation result containing the computed Number or an error.
        """
        res = RunTimeResult()
        left_node = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right_node = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        error = None
        if node.operator.type == T_PLUS:
            result, error = left_node.add(right_node)
        elif node.operator.type == T_MINUS:
            result, error = left_node.subtract(right_node)
        elif node.operator.type == T_MUL:
            result, error = left_node.multiply(right_node)
        elif node.operator.type == T_DIVIDE:
            result, error = left_node.divide(right_node)
        elif node.operator.type == T_EXP:
            result, error = left_node.exponent(right_node)
        elif node.operator.type == T_EE:
            result, error = left_node.get_comparison_eq(right_node)
        elif node.operator.type == T_NEQ:
            result, error = left_node.get_comparison_neq(right_node)
        elif node.operator.type == T_GT:
            result, error = left_node.get_comparison_gt(right_node)
        elif node.operator.type == T_GTE:
            result, error = left_node.get_comparison_gte(right_node)
        elif node.operator.type == T_LT:
            result, error = left_node.get_comparison_lt(right_node)
        elif node.operator.type == T_LTE:
            result, error = left_node.get_comparison_lte(right_node)
        elif node.operator.type == T_KEYWORD and node.operator.value == 'and':
            result, error = left_node.and_by(right_node)
        elif node.operator.type == T_KEYWORD and node.operator.value == 'or':
            result, error = left_node.or_by(right_node)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOperationNode(self, node, context):
        """
        Evaluates a unary operation node (e.g., negation).

        Parameters:
        - node (UnaryOperationNode): The unary operation node.
        - context (Context): The execution context.

        Returns:
        - RunTimeResult: The evaluation result containing the computed Number or an error.
        """
        res = RunTimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        error = None
        if node.operator.type == T_MINUS:
            number, error = number.multiply(Number(-1))

        elif node.operator.type == T_KEYWORD and node.operator.value == 'not':
            number, error = number.not_by()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
