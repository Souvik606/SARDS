class SwitchNode:
    def __init__(self, cases, default_case, return_null):
        self.cases = cases
        self.default_case = default_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.default_case or self.cases[-1])[0].pos_end
        self.return_null = return_null


class CaseNode:
    def __init__(self, dash):
        self.dash = dash
