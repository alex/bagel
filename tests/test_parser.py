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

    def visit_assignment(self, node1, node2):
        self.visit(node1._target, node2._target)
        self.visit(node1._value, node2._value)

    def visit_match(self, node1, node2):
        self.visit(node1._condition, node2._condition)
        self._visit_list(node1._cases, node2._cases)

    def visit_match_case(self, node1, node2):
        self.visit(node1._matcher, node2._matcher)
        self.visit(node1._body, node2._body)

    def visit_if(self, node1, node2):
        self.visit(node1._condition, node2._condition)
        self.visit(node1._if_body, node2._if_body)

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

    def visit_binop(self, node1, node2):
        assert node1._op == node2._op
        self.visit(node1._lhs, node2._lhs)
        self.visit(node1._rhs, node2._rhs)

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
    def test_no_conflicts(self):
        assert not parser.Parser._parser.lr_table.sr_conflicts
        assert not parser.Parser._parser.lr_table.rr_conflicts

    def test_simple_function(self):
        assert_parses("""
        def f():
            return 3
        """, ast.Module([
            ast.Function("f", [], None, ast.Suite([
                ast.Return(ast.Integer(3)),
            ]))
        ]))

    def test_function_return_type(self):
        assert_parses("""
        def f() -> Int:
            return 3
        """, ast.Module([
            ast.Function("f", [], ast.Name("Int"), ast.Suite([
                ast.Return(ast.Integer(3))
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

    def test_match_statement(self):
        assert_parses("""
        def f():
            match 3:
                with n:
                    return n
        """, ast.Module([
            ast.Function("f", [], None, ast.Suite([
                ast.Match(ast.Integer(3), [
                    ast.MatchCase(ast.Name("n"), ast.Suite([
                        ast.Return(ast.Name("n"))
                    ]))
                ])
            ]))
        ]))

    def test_match_multiple_cases(self):
        assert_parses("""
        def f():
            match 3:
                with 5:
                    return 10
                with n:
                    return n
        """, ast.Module([
            ast.Function("f", [], None, ast.Suite([
                ast.Match(ast.Integer(3), [
                    ast.MatchCase(ast.Integer(5), ast.Suite([
                        ast.Return(ast.Integer(10))
                    ])),
                    ast.MatchCase(ast.Name("n"), ast.Suite([
                        ast.Return(ast.Name("n"))
                    ]))
                ])
            ]))
        ]))

    def test_assignment(self):
        assert_parses("""
        def f():
            a = 2
        """, ast.Module([
            ast.Function("f", [], None, ast.Suite([
                ast.Assignment(ast.Name("a"), ast.Integer(2))
            ]))
        ]))

    def test_binop(self):
        assert_parses("""
        def f():
            4 + 8
        """, ast.Module([
            ast.Function("f", [], None, ast.Suite([
                ast.BinOp("+", ast.Integer(4), ast.Integer(8))
            ]))
        ]))

    def test_if_statement(self):
        assert_parses("""
        def f():
            if 3:
                a = 4
        """, ast.Module([
            ast.Function("f", [], None, ast.Suite([
                ast.If(
                    ast.Integer(3),
                    ast.Suite([ast.Assignment(ast.Name("a"), ast.Integer(4))]),
                ),
            ]))
        ]))
