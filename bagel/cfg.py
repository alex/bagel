import enum


class Opcodes(enum.Enum):
    ASSIGN = 0

    ADD = 1


class Namespace(object):
    def __init__(self):
        self._functions = {}

    def new_function(self, name, arguments):
        self._functions[name] = func = Function()
        return func

    def find_function(self, name):
        return self._functions[name]

    def visit(self, node, arg):
        return node.visit(self, arg)

    def _visit_list(self, items, arg):
        for item in items:
            self.visit(item, arg)

    def visit_module(self, node, arg):
        self._visit_list(node._declarations, arg)

    def visit_function(self, node, arg):
        function = self.new_function(node._name, node._arguments)
        function._entry_block.visit(node._body, None)


class Function(object):
    def __init__(self):
        self._block_counter = 0
        self._temporary_counter = 0
        self._entry_block = Block(self)

    def new_temporary_name(self):
        result = "v{:d}".format(self._temporary_counter)
        self._temporary_counter += 1
        return result

    def new_block_name(self):
        result = "B{:d}".format(self._block_counter)
        self._block_counter += 1
        return result


class Block(object):
    def __init__(self, function):
        self._name = function.new_block_name()
        self._function = function
        self._instructions = []
        self._exit_condition = None

    def emit(self, instruction):
        assert self._exit_condition is None
        self._instructions.append(instruction)

    def exit(self, cond):
        assert self._exit_condition is None
        self._exit_condition = cond

    def has_exit(self):
        return self._exit_condition is not None

    def new_temporary(self):
        return InstructionResult(self._function.new_temporary_name())

    def new_block(self):
        return Block(self._function)

    def visit(self, node, arg):
        return node.visit(self, arg)

    def _visit_list(self, items, arg):
        for item in items:
            self.visit(item, arg)

    def visit_suite(self, node, arg):
        self._visit_list(node._body, arg)

    def visit_return(self, node, arg):
        v = self.visit(node._value, arg)
        self.exit(ReturnValue(v))

    def visit_if(self, node, arg):
        v = self.visit(node._condition, arg)
        if_block = self.new_block()
        else_block = self.new_block()

        self.exit(ConditionalBranch(v, if_block, else_block))

        if_block.visit(node._if_body, arg)
        # TODO: handle fallthroug block
        assert if_block.has_exit()

        else_block.visit(node._else_body, arg)
        assert else_block.has_exit()

    def visit_assignment(self, node, arg):
        # TODO: handle the fact that this is an assignment context
        v1 = self.visit(node._target, arg)
        v2 = self.visit(node._value, arg)
        self.emit(Instruction(Opcodes.ASSIGN, [v2], v1))

    def visit_binop(self, node, arg):
        v1 = self.visit(node._lhs, arg)
        v2 = self.visit(node._rhs, arg)
        result = self.new_temporary()
        op = {
            "+": Opcodes.ADD,
        }[node._op]
        self.emit(Instruction(op, [v1, v2], result=result))
        return result

    def visit_name(self, node, arg):
        # TODO: figure out if the name is a local, update the symbol table,
        # etc.
        return LocalName(node._value)

    def visit_integer(self, node, arg):
        return ConstantInt(node._value)



class Instruction(object):
    def __init__(self, opcode, arguments, result=None):
        self._opcode = opcode
        self._arguments = arguments
        self._result = result


class ReturnValue(object):
    def __init__(self, value):
        self._value = value


class ConditionalBranch(object):
    def __init__(self, condition, if_target, else_target):
        self._condition = condition
        self._if_target = if_target
        self._else_target = else_target


class LocalName(object):
    def __init__(self, name):
        self._name = name


class ConstantInt(object):
    def __init__(self, value):
        self._value = value


class InstructionResult(object):
    def __init__(self, name):
        self._name = name
