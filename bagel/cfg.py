import enum

# enum type Opcode:
#     # ...


# enum type Value:
#     case LocalVariable(name: Text)
#     case GlobalName(name: Text)
#     case ConstantInt(value: Int)
#     case Temporary(number: Int)


# class type Instruction:
#     op: Opcode
#     arguments: List[Value]
#     result: Option[Value]


# enum type ExitCondition:
#     case ReturnValue(Option[Value])
#     case Jump(Block)
#     case If(cond: Value, if_target: Block, else_target: Block)


# class type Block:
#     instructions: List[Instruction]
#     exit_condition: ExitCondition


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


class InstructionBuilder(object):
    def __init__(self, function, block):
        self._function = function
        self._block = block

    def emit(self, instruction):
        self._block.emit(instruction)

    def exit(self, exit_condition):
        self._block.exit(exit_condition)

    def new_temporary(self):
        return self._block.new_temporary()

    def has_exit(self):
        return self._block.has_exit()

    def new_block(self):
        return Block(self._function)

    def use_block(self, block):
        self._block = block


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


class ASTToControlFlowVisitor(object):
    def visit(self, node, arg):
        return node.visit(self, arg)

    def _visit_list(self, items, arg):
        for item in items:
            self.visit(item, arg)

    def visit_module(self, node, namespace):
        self._visit_list(node._declarations, namespace)

    def visit_function(self, node, namespace):
        function = namespace.new_function(node._name, node._arguments)
        self.visit(node._body, InstructionBuilder(function, function._entry_block))

    def visit_suite(self, node, builder):
        self._visit_list(node._body, builder)

    def visit_return(self, node, builder):
        v = self.visit(node._value, builder)
        builder.exit(ReturnValue(v))

    def visit_if(self, node, builder):
        v = self.visit(node._condition, builder)
        if_block = builder.new_block()
        else_block = builder.new_block()

        builder.exit(ConditionalBranch(v, if_block, else_block))

        builder.use_block(if_block)
        self.visit(node._if_body, builder)
        # TODO: handle fallthroug block
        assert builder.has_exit()

        builder.use_block(else_block)
        self.visit(node._else_body, builder)
        assert builder.has_exit()

    def visit_assignment(self, node, builder):
        # TODO: handle the fact that this is an assignment context
        v1 = self.visit(node._target, builder)
        v2 = self.visit(node._value, builder)
        builder.emit(Instruction(Opcodes.ASSIGN, [v2], v1))

    def visit_binop(self, node, builder):
        v1 = self.visit(node._lhs, builder)
        v2 = self.visit(node._rhs, builder)
        result = builder.new_temporary()
        op = {
            "+": Opcodes.ADD,
        }[node._op]
        builder.emit(Instruction(op, [v1, v2], result=result))
        return result

    def visit_name(self, node, builder):
        # TODO: figure out if the name is a local, update the symbol table,
        # etc.
        return LocalName(node._value)

    def visit_integer(self, node, builder):
        return ConstantInt(node._value)
