import textwrap

from bagel import cfg, parser


class Function(object):
    def __init__(self, name, arguments, blocks):
        self._name = name
        self._arguments = arguments
        self._blocks = blocks

    def __eq__(self, other):
        return self._blocks[0] == other._entry_block


class Block(object):
    def __init__(self, instructions, exit_condition):
        self._instructions = instructions
        self._exit_condition = exit_condition

    def __eq__(self, other):
        return (
            self._instructions == other._instructions and
            self._exit_condition == other._exit_condition
        )


def assert_lowers(source, expected_function):
    source = textwrap.dedent(source).lstrip()
    ast = parser.Parser().parse(source)
    namespace = cfg.Namespace()
    cfg.ASTToControlFlowVisitor().visit(ast, namespace)

    assert expected_function == namespace.find_function("f")


class TestCFGLowering(object):
    def test_simple_function(self):
        assert_lowers("""
        def f() -> Int:
            return 3
        """, Function("f", [], [
            Block([], exit_condition=cfg.ReturnValue(cfg.ConstantInt(3)))
        ]))

    def test_assignment(self):
        assert_lowers("""
        def f() -> Int:
            a = 3
            return a
        """, Function("f", [], [
            Block([
                cfg.Instruction(
                    cfg.Opcodes.ASSIGN,
                    [cfg.LocalName("a"), cfg.ConstantInt(3)]
                ),
            ], exit_condition=cfg.ReturnValue(cfg.LocalName("a")))
        ]))

    def test_lower_assignment_arithmetic(self):
        assert_lowers("""
        def f() -> Int:
            a = 3
            b = 5
            c = a + b
            return 4 + c
        """, Function("f", [], [
            Block([
                cfg.Instruction(
                    cfg.Opcodes.ASSIGN,
                    [cfg.LocalName("a"), cfg.ConstantInt(3)]
                ),
                cfg.Instruction(
                    cfg.Opcodes.ASSIGN,
                    [cfg.LocalName("b"), cfg.ConstantInt(5)]
                ),
                cfg.Instruction(
                    cfg.Opcodes.ADD,
                    [cfg.LocalName("a"), cfg.LocalName("b")],
                    result=cfg.InstructionResult("v0")
                ),
                cfg.Instruction(
                    cfg.Opcodes.ASSIGN,
                    [cfg.LocalName("c"), cfg.InstructionResult("v0")]
                ),
                cfg.Instruction(
                    cfg.Opcodes.ADD,
                    [cfg.ConstantInt(4), cfg.LocalName("c")],
                    result=cfg.InstructionResult("v1")
                ),
            ], exit_condition=cfg.ReturnValue(cfg.InstructionResult("v1")))
        ]))
