"""
This module defines the ForNode class, which represents
a 'for' loop node in the abstract syntax tree (AST).

Classes:
    ForNode: A class to represent a 'for' loop node in the AST.
"""
class ForNode: # pylint: disable=R0903
    """
    Represents a 'for' loop node in the abstract syntax tree (AST).

    Attributes:
        var_name_tok: The token representing the loop variable name.
        start_value_node: The node representing the start value of the loop.
        end_value_node: The node representing the end value of the loop.
        step_value_node: The node representing the step value of the loop.
        body_node: The node representing the body of the loop.
        pos_start: The starting position of the 'for' loop in the source code.
        pos_end: The ending position of the 'for' loop in the source code.
        return_null: A flag indicating whether the loop returns null.
    """
    def __init__(self, var_name_tok, start_value_node,
                 end_value_node, step_value_node, body_node, return_null):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end
        self.return_null = return_null
