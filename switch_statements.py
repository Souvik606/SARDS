class SwitchNode:
    def __init__(self, select, cases, return_null):
        self.select = select
        self.cases = cases
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = self.cases[-1][0].pos_end
        self.return_null = return_null
