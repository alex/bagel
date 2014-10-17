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
