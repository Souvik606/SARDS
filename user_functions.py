class FunctionDefinitionNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node, auto_return):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.auto_return = auto_return

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end


class FunctionCallNode:
    def __init__(self, call_node, arg_nodes):
        self.call_node = call_node
        self.arg_nodes = arg_nodes

        self.pos_start = self.call_node.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[-1].pos_end
        else:
            self.pos_end = self.call_node.pos_end
