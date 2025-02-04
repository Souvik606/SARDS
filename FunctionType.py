from variablesNode import *
from Error_Class import RunTimeError


class Function:
    def __init__(self, name, body_node, arg_names):
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def execute(self, args):
        from Interpreter import RunTimeResult,Interpreter,Context

        res = RunTimeResult()
        interpreter = Interpreter()
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args)>len(self.arg_names):
            return res.failure(RunTimeError(self.pos_start,self.pos_end,
                                f"{len(args)-len(self.arg_names)} too few args passed into '{self.name}'",self.context))

        if len(args) < len(self.arg_names):
            return res.failure(RunTimeError(self.pos_start, self.pos_end,
                                f"{len(self.arg_names) - len(args)} too few args passed into '{self.name}'",
                                            self.context))

        for i in range(len(args)):
            arg_name=self.arg_names[i]
            arg_value=args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name,arg_value)

        value=res.register(interpreter.visit(self.body_node,new_context))
        if res.error:return res
        return res.success(value)

    def copy(self):
        copy=Function(self.name,self.body_node,self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start,self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"
