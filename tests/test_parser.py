import textwrap

from bagel import ast, parser


class AssertEqualVisitor(object):
    def visit(self, node, arg):
        if node is not arg:
            node.visit(self, arg)

    def _visit_list(self, a1, a2):
        if a1 is not a2:
            assert len(a1) == len(a2)
            for a, b in zip(a1, a2):
                self.visit(a, b)

    def visit_module(self, node1, node2):
        self._visit_list(node1._declarations, node2._declarations)

    def visit_function(self, node1, node2):
        assert node1._name == node2._name
        assert node1._arguments == node2._arguments
        self.visit(node1._return_type, node2._return_type)
        self.visit(node1._body, node2._body)

    def visit_suite(self, node1, node2):
        self._visit_list(node1._body, node2._body)

    def visit_return(self, node1, node2):
        self.visit(node1._value, node2._value)

    def visit_class(self, node1, node2):
        assert node1._name == node2._name
        self._visit_list(node1._declarations, node2._declarations)

    def visit_attribute(self, node1, node2):
        assert node1._name == node2._name
        self.visit(node1._tp, node2._tp)

    def visit_enum(self, node1, node2):
        assert node1._name == node2._name
        self._visit_list(node1._cases, node2._cases)

    def visit_enum_case(self, node1, node2):
        assert node1._name == node2._name
        self._visit_list(node1._members, node2._members)

    def visit_name(self, node1, node2):
        assert node1._value == node2._value

    def visit_integer(self, node1, node2):
        assert node1._value == node2._value


def assert_parses(source, expected_ast):
    source = textwrap.dedent(source).lstrip()
    p = parser.Parser()
    actual_ast = p.parse(source)
    AssertEqualVisitor().visit(actual_ast, expected_ast)


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
