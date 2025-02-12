"""
This module defines the SwitchNode class, which represents
a node for switch statement in the abstract syntax tree (AST).

Classes:
    SwitchNode: A class to represent a switch statement node in the AST.
"""
class SwitchNode: # pylint: disable=R0903
    """
    Represents a switch statement node in the abstract syntax tree (AST).

    Attributes:
        select: The node representing the value to be matched with cases.
        cases: The node representing the list of cases in the switch statement.
        pos_start: The starting position of the switch statement in the source code.
        pos_end: The ending position of the switch statement in the source code.
        return_null: A flag indicating whether the statement returns null.
    """
    def __init__(self, select, cases, return_null):
        self.select = select
        self.cases = cases
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = self.cases[-1][0].pos_end
        self.return_null = return_null
