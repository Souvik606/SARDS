class SwitchNode:
    def __init__(self, select, cases, default_case, index_def, count, return_null):
        self.select = select
        self.cases = cases
        self.default_case = default_case
        #self.body_cases = body_cases
        #self.default_body = default_body
        self.index_def = index_def
        self.count = count
        self.pos_start = self.default_case.pos_start if index_def == 0 else self.cases.pos_start 
        self.pos_end = self.default_case.pos_end if index_def == count-1 else self.cases.pos_end
        self.return_null = return_null

'''
class CaseNode:
    def __init__(self, choice_node, body_node, return_null):
        self.choice_node = choice_node
        self.body_node = body_node
        self.pos_start = self.choice_node.pos_start
        self.pos_end = self.body_node.pos_end
        self.return_null = return_null
'''