class ReturnNode:
    def __init__(self,node_to_return,pos_start,pos_end):
        self.node_to_return=node_to_return
        self.pos_start=pos_start
        self.pos_end=pos_end

class ContinueNode:
    def __init__(self,pos_start,pos_end):
        self.pos_start=pos_start
        self.pos_end=pos_end

class BreakNode:
    def __init__(self,pos_start,pos_end):
        self.pos_start=pos_start
        self.pos_end=pos_end