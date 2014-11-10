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
