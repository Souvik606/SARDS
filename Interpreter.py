"""
interpreter.py

This module defines the components needed for interpreting an abstract syntax tree (AST).
It includes classes for handling runtime context, execution results, and evaluating expressions.

Classes:
- Context: Maintains execution context (e.g., scope, parent context).
- RunTimeResult: Stores the result of an evaluation, including errors.
- Interpreter: Evaluates AST nodes and executes operations.
"""

from NumberDataType import Number
from constants import T_PLUS, T_MINUS, T_MUL, T_DIVIDE


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

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
