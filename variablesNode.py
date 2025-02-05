class SymbolTable:
    def __init__(self,parent=None):
        self.symbols={}
        self.parent=parent

    def get(self,name):
        value=self.symbols.get(name,None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self,name,value):
        self.symbols[name]=value

    def remove(self,name):
        del self.symbols[name]


#Variable_Nodes
class VariableUseNode:
    def __init__(self,var_name_tok):
        self.var_name_tok=var_name_tok
        self.pos_start=self.var_name_tok.pos_start
        self.pos_end=self.var_name_tok.pos_end

    def __repr__(self):
        return f'({self.var_name_tok.value})'

class VariableAssignNode:
    def __init__(self,var_name_tok,value_node):
        self.var_name_tok=var_name_tok
        self.value_node=value_node
        self.pos_start=self.var_name_tok.pos_start
        self.pos_end=self.value_node.pos_end

    def __repr__(self):
        return f'({self.var_name_tok.value}:{self.value_node})'
