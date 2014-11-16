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
        -> 3
        """)

    def test_assignment(self):
        assert_lowers("""
        def f() -> Int:
            a = 3
            return a
        """, """
        B1:
        a = 3
        -> a
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
        a = 3
        b = 5
        @v1 = add(a, b)
        c = @v1
        @v2 = add(4, c)
        -> @v2
        """)
