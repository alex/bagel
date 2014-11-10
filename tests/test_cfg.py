import textwrap

from bagel import parser

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
#     case If(cond: Value, if_target: Block, else_target: Block)



# class type Block:
#     instructions: List[Instruction]
#     exit_condition: ExitCondition


# class type Function:
#     entry_block: Block
#     arguments: List[Value]


class Function(object):
    def __init__(self, name, arguments, blocks):
        self._name = name
        self._arguments = arguments
        self._blocks = blocks


class Block(object):
    def __init__(self, instructions, exit_condition):
        self._instructions = instructions
        self._exit_condition = exit_condition


class ReturnValue(object):
    def __init__(self, value):
        self._value = value


class ConstantInt(object):
    def __init__(self, value):
        self._value = value


def assert_lowers(source, expected_cfg):
    source = textwrap.dedent(source).lstrip()
    ast = parser.Parser().parse(source)
    namespace = ControlFlowVisitor().visit(ast)
    assert namespace.find_function("f") == expected_cfg


class TestCFGLowering(object):
    def test_simple_function(self):
        assert_lowers("""
        def f() -> Int:
            return 3
        """, Function("f", [], [
            Block([], exit_condition=ReturnValue(ConstantInt(3)))
        ]))
