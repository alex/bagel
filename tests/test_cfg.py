import textwrap

from bagel import cfg, parser


def assert_lowers(source, expected_function):
    source = textwrap.dedent(source).lstrip()
    ast = parser.Parser().parse(source)
    namespace = cfg.Namespace()
    cfg.ASTToControlFlowVisitor().visit(ast, namespace)

    # TODO: parse the expected function
    assert expected_function == namespace.find_function("f")


class TestCFGLowering(object):
    def test_simple_function(self):
        assert_lowers("""
        def f() -> Int:
            return 3
        """, """
        B1:
        :RETURN 3
        """)

    def test_assignment(self):
        assert_lowers("""
        def f() -> Int:
            a = 3
            return a
        """, """
        B1:
        ASSIGN a -> 3
        :RETURN a
        """)

    def test_lower_assignment_arithmetic(self):
        assert_lowers("""
        def f() -> Int:
            a = 3
            b = 5
            c = a + b
            return 4 + c
        """, """
        B1:
        ASSIGN 3 -> a
        ASSIGN b -> 5
        ADD a, b -> @v1
        ASSIGN @v1 -> c
        ADD 4, c -> @v2
        :RETURN @v2
        """)
