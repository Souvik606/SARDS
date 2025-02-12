from sards.ast_nodes import *
from sards.core import *
from sards.data_types import *


class BaseFunction():
    def __init__(self, name):
        self.name = name or "<anonymous>"
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def generate_new_context(self):
        from sards.core import Context

        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RunTimeResult()

        if len(args) > len(arg_names):
            return res.failure(RunTimeError(self.pos_start, self.pos_end,
                                            f"{len(args) - len(self.arg_names)} too few args passed into '{self.name}'",
                                            self.context))

        if len(args) < len(arg_names):
            return res.failure(RunTimeError(self.pos_start, self.pos_end,
                                            f"{len(self.arg_names) - len(args)} too few args passed into '{self.name}'",
                                            self.context))
        return res.success(None)

    def populate_args(self, arg_names, args, context):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(context)
            context.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, context):
        res = RunTimeResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, context)
        return res.success(None)


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.auto_return = auto_return

    def execute(self, args):
        from sards.core import RunTimeResult, Interpreter

        res = RunTimeResult()
        interpreter = Interpreter()
        exec_context = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_context))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, exec_context))
        if res.should_return() and res.func_return_value == None: return res

        return_value = (value if self.auto_return else None) or res.func_return_value or Number(0)
        return res.success(return_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RunTimeResult()
        exec_context = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_context))
        if res.should_return(): return res

        return_value = res.register(method(exec_context))
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    def execute_show(self, exec_context):
        print(str(exec_context.symbol_table.get('value')))
        return RunTimeResult().success(Number(0))

    execute_show.arg_names = ['value']

    def execute_listen(self, exec_context):
        text = input()
        return RunTimeResult().success(String(text))

    execute_listen.arg_names = []

    def execute_Integer(self, exec_context):
        try:
            number = int(exec_context.symbol_table.get('value').value)
        except ValueError:
            raise Exception("Value Error: Cant convert to integer")

        return RunTimeResult().success(Number(number))

    execute_Integer.arg_names = ['value']

    def execute_String(self, exec_context):
        try:
            string = str(exec_context.symbol_table.get('value').value)
        except ValueError:
            raise Exception("Value Error: Cant convert to string")

        return RunTimeResult().success(String(string))

    execute_String.arg_names = ['value']

    def execute_type(self, exec_context):
        data = exec_context.symbol_table.get('value')
        if isinstance(data, Number):
            print("type <Number>")
        elif isinstance(data, String):
            print("type <String>")
        elif isinstance(data, List):
            print("type <List>")
        return RunTimeResult().success(Number(0))

    execute_type.arg_names = ['value']


BuiltInFunction.show = BuiltInFunction('show')
BuiltInFunction.listen = BuiltInFunction('listen')
BuiltInFunction.Integer = BuiltInFunction('Integer')
BuiltInFunction.String = BuiltInFunction('String')
BuiltInFunction.type = BuiltInFunction('type')
