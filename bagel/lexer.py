from rply import LexerGenerator
from rply.token import Token


class Lexer(object):
    _lg = LexerGenerator()
    _lg.add("DEF", r"def")
    _lg.add("TYPE", r"type")
    _lg.add("CLASS", r"class")
    _lg.add("ENUM", r"enum")
    _lg.add("MATCH", r"match")
    _lg.add("WITH", r"with"),
    _lg.add("CASE", r"case")
    _lg.add("RETURN", r"return")
    _lg.add("IF", r"if")

    _lg.add("LPAREN", r"\(")
    _lg.add("RPAREN", r"\)")

    _lg.add("COLON", r":")
    _lg.add("COMMA", r",")
    _lg.add("ARROW", r"->")
    _lg.add("EQUAL", r"=")

    _lg.add("PLUS", r"\+")

    _lg.add("INTEGER", r"\d+")

    _lg.add("NEWLINE_WITH_SPACES", r"\n(    )*")

    _lg.add("NAME", r"[a-zA-Z]+")

    _lg.ignore(r" ")

    _lexer = _lg.build()

    def lex(self, source):
        return self._translate_indentation(self._lexer.lex(source))

    def _translate_indentation(self, token_stream):
        levels = 0
        for token in token_stream:
            if token.name == "NEWLINE_WITH_SPACES":
                yield Token("NEWLINE", "\n", token.source_pos)
                num_indent_blocks = len(token.value[1:]) / 4
                if num_indent_blocks > levels:
                    for i in range(num_indent_blocks - levels):
                        yield Token("INDENT", "    ", token.source_pos)
                    levels = num_indent_blocks
                elif num_indent_blocks < levels:
                    for i in range(levels - num_indent_blocks):
                        yield Token("DEDENT", "", token.source_pos)
                    levels = num_indent_blocks
            else:
                yield token
