import textwrap

from bagel import ast, parser


def assert_parses(source, expected_ast):
    source = textwrap.dedent(source).lstrip()
    p = parser.Parser()
    actual_ast = p.parse(source)
    assert actual_ast == expected_ast


class TestParser(object):
    def test_simple_function(self):
        assert_parses("""
        def f():
            return 3
        """, ast.Module([
            ast.Function("f", [], None, ast.Suite([
                ast.Return(ast.Integer(3)),
            ]))
        ]))

    def test_simple_class(self):
        assert_parses("""
        class type Foo:
            a: Int
        """, ast.Module([
            ast.Class("Foo", [
                ast.Attribute("a", ast.Name("Int")),
            ])
        ]))

    def test_enum(self):
        assert_parses("""
        enum type Foo:
            case Bar
            case Baz(Int, Int)
        """, ast.Module([
            ast.Enum("Foo", [
                ast.EnumCase("Bar"),
                ast.EnumCase("Baz", [ast.Name("Int"), ast.Name("Int")])
            ])
        ]))
