# enum type Opcode:
#     # ...


# interface type Value:
#     case LocalVariable(name: Text)
#     case GlobalName(name: Text)
#     case ConstantInt(value: Int)


# class type Instruction:
#     op: Opcode
#     arguments: List[Value]
#     result: Option[Value]


# enum type ExitCondition:
#     case ReturnValue(Option[Value])
#     case Fallthrough(Block)
#     case If(cond: Value, if_target: Block, else_target: Block)



# class type Block:
#     instructions: List[Instruction]
#     exit_condition: ExitCondition

class Namespace(object):
    def __init__(self):
        self._functions = {}

    def new_function(self, name, arguments):
        self._functions[name] = func = Function()
        return func._entry_block

    def find_function(self, name):
        return self._functions[name]


class Function(object):
    def __init__(self):
        self._entry_block = Block()


class Block(object):
    def __init__(self):
        self._instructions = []
        self._exit_condition = None

    def exit(self, cond):
        assert self._exit_condition is None
        self._exit_condition = cond


class ReturnValue(object):
    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        return self._value == other._value


class ConstantInt(object):
    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        return self._value == other._value


class ASTToControlFlowVisitor(object):
    def visit(self, node, arg):
        return node.visit(self, arg)

    def _visit_list(self, items, arg):
        for item in items:
            self.visit(item, arg)

    def visit_module(self, node, namespace):
        self._visit_list(node._declarations, namespace)

    def visit_function(self, node, namespace):
        builder = namespace.new_function(node._name, node._arguments)
        self.visit(node._body, builder)

    def visit_suite(self, node, builder):
        self._visit_list(node._body, builder)

    def visit_return(self, node, builder):
        v = self.visit(node._value, builder)
        builder.exit(ReturnValue(v))

    def visit_integer(self, node, builder):
        return ConstantInt(node._value)
