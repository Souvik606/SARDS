from .number_type import Number
from .string_type import String


class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.element_nodes])}]'


class List:
    def __init__(self, elements):
        self.elements = elements
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add(self, operand):
        if isinstance(operand, Number) or isinstance(operand, String):
            new_list = self.copy()
            new_list.elements.append(operand)
            return new_list, None

        elif isinstance(operand, List):
            new_list = self.copy()
            for i in operand.elements:
                new_list.elements.append(i)
            return new_list, None

    def subtract(self, operand):
        if isinstance(operand, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(operand.value)
                return new_list, None
            except:
                return None, RuntimeError(operand.pos_start, operand.pos_end,
                                          'Index out of bounds', self.context)

    def multiply(self, operand):
        if isinstance(operand, Number):
            new_list = self.copy()
            new_list.elements = new_list.elements * operand.value
            return new_list, None

    def is_true(self):
        return len(self.elements) > 0

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
