import textwrap

from rply.token import Token

from bagel import lexer


def assert_lexes(source, expected_tokens):
    source = textwrap.dedent(source).lstrip()
    l = lexer.Lexer()
    tokens = list(l.lex(source))
    assert tokens == expected_tokens


class TestLexer(object):
    def test_simple_function(self):
        assert_lexes("""
        def f():
            return 3
        """, [
            Token("DEF", "def"),
            Token("NAME", "f"),
            Token("LPAREN", "("),
            Token("RPAREN", ")"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("RETURN", "return"),
            Token("INTEGER", "3"),
            Token("NEWLINE", "\n"),
            Token("DEDENT", ""),
        ])

    def test_multiple_lines_at_indentation_level(self):
        assert_lexes("""
        def f():
            return 3
            return 4
        """, [
            Token("DEF", "def"),
            Token("NAME", "f"),
            Token("LPAREN", "("),
            Token("RPAREN", ")"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("RETURN", "return"),
            Token("INTEGER", "3"),
            Token("NEWLINE", "\n"),
            Token("RETURN", "return"),
            Token("INTEGER", "4"),
            Token("NEWLINE", "\n"),
            Token("DEDENT", ""),
        ])

    def test_multi_level_indent_dedent(self):
        assert_lexes("""
        def f():
            def g():
                return 3
        """, [
            Token("DEF", "def"),
            Token("NAME", "f"),
            Token("LPAREN", "("),
            Token("RPAREN", ")"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("DEF", "def"),
            Token("NAME", "g"),
            Token("LPAREN", "("),
            Token("RPAREN", ")"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("RETURN", "return"),
            Token("INTEGER", "3"),
            Token("NEWLINE", "\n"),
            Token("DEDENT", ""),
            Token("DEDENT", ""),
        ])

    def test_class(self):
        assert_lexes("""
        class type Foo:
            a: Int
        """, [
            Token("CLASS", "class"),
            Token("TYPE", "type"),
            Token("NAME", "Foo"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("NAME", "a"),
            Token("COLON", ":"),
            Token("NAME", "Int"),
            Token("NEWLINE", "\n"),
            Token("DEDENT", ""),
        ])

    def test_enum(self):
        assert_lexes("""
        enum type Foo:
            case Bar
            case Baz(Int, Int)
        """, [
            Token("ENUM", "enum"),
            Token("TYPE", "type"),
            Token("NAME", "Foo"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("CASE", "case"),
            Token("NAME", "Bar"),
            Token("NEWLINE", "\n"),
            Token("CASE", "case"),
            Token("NAME", "Baz"),
            Token("LPAREN", "("),
            Token("NAME", "Int"),
            Token("COMMA", ","),
            Token("NAME", "Int"),
            Token("RPAREN", ")"),
            Token("NEWLINE", "\n"),
            Token("DEDENT", ""),
        ])

    def test_function_return_type(self):
        assert_lexes("""
        def f() -> Int:
            return 3
        """, [
            Token("DEF", "def"),
            Token("NAME", "f"),
            Token("LPAREN", "("),
            Token("RPAREN", ")"),
            Token("ARROW", "->"),
            Token("NAME", "Int"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("RETURN", "return"),
            Token("INTEGER", "3"),
            Token("NEWLINE", "\n"),
            Token("DEDENT", ""),
        ])

    def test_match_statement(self):
        assert_lexes("""
        def f():
            match 3:
                as n:
                    return n
        """, [
            Token("DEF", "def"),
            Token("NAME", "f"),
            Token("LPAREN", "("),
            Token("RPAREN", ")"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("MATCH", "match"),
            Token("INTEGER", "3"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("AS", "as"),
            Token("NAME", "n"),
            Token("COLON", ":"),
            Token("NEWLINE", "\n"),
            Token("INDENT", "    "),
            Token("RETURN", "return"),
            Token("NAME", "n"),
            Token("NEWLINE", "\n"),
            Token("DEDENT", ""),
            Token("DEDENT", ""),
            Token("DEDENT", ""),
        ])
