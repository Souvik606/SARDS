class SwitchNode:
    def __init__(self, select, cases, default_case, return_null):
        self.select = select
        self.cases = cases
        self.default_case = default_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.default_case or self.cases[-1])[0].pos_end
        self.return_null = return_null


class CaseNode:
    def __init__(self, choice_node, body_node, return_null):
        self.choice_node = choice_node
        self.body_node = body_node
        self.pos_start = self.choice_node.pos_start
        self.pos_end = self.body_node.pos_end
        self.return_null = return_null
