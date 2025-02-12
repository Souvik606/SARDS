"""
This module defines the IfNode class, which represents
an 'if-elif-else' statement node in the abstract syntax tree (AST).

Classes:
    IfNode: A class to represent an 'if-elif-else' statement node in the AST.
"""
class IfNode: # pylint: disable=R0903
    """
    Represents an 'if' statement node in the abstract syntax tree (AST).

    Attributes:
        cases: A list of tuples, each containing a condition node and a body
               node for each 'if' and 'elif' case.
        else_case: The node representing the 'else' case, if any.
        pos_start: The starting position of the 'if' statement in the source code.
        pos_end: The ending position of the 'if' statement in the source code.
    """
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[-1])[0].pos_end
