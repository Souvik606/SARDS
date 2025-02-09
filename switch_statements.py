class SwitchNode:
    def __init__(self, selection, cases, default_case):
        self.cases = cases
        self.selection = selection
        self.default_case = default_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.default_case or self.cases[-1])[0].pos_end

    def __repr__(self):
        return f'cases:{self.cases} ; selection:{self.selection} ; default:{self.default_case}'
