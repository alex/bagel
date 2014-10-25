from rply import ParserGenerator

from bagel import ast, lexer


class Parser(object):
    _pg = ParserGenerator([
        "NEWLINE", "INDENT", "DEDENT",

        "COLON",

        "LPAREN", "RPAREN",

        "DEF", "RETURN",

        "NAME", "INTEGER",
    ])

    @_pg.production("program : module")
    def program_module(self, p):
        return p[0]

    @_pg.production("module : declerations")
    def module_declerations(self, p):
        return ast.Module(p[0])

    @_pg.production("declerations : none")
    def declerations_none(self, p):
        return []

    @_pg.production("declerations : declerations decleration")
    def declerations_declerations_decleration(self, p):
        return p[0] + [p[1]]

    @_pg.production("decleration : function")
    def module_decleration(self, p):
        return p[0]

    @_pg.production("function : DEF NAME LPAREN RPAREN COLON NEWLINE INDENT suite DEDENT")
    def module_function(self, p):
        return ast.Function(
            p[1].getstr(), [], None, p[7],
        )

    @_pg.production("suite : statements")
    def suite_statements(self, p):
        return ast.Suite(p[0])

    @_pg.production("statements : none")
    def statements_none(self, p):
        return []

    @_pg.production("statements : statements statement")
    def statements_statements_statement(self, p):
        return p[0] + [p[1]]

    @_pg.production("statement : RETURN expression NEWLINE")
    def statement_return_expression_newline(self, p):
        return ast.Return(p[1])

    @_pg.production("expression : INTEGER")
    def expression_integer(self, p):
        return ast.Integer(int(p[0].getstr()))

    @_pg.production("none : ")
    def none(self, p):
        return None

    _parser = _pg.build()

    def parse(self, source):
        tokens = lexer.Lexer().lex(source)
        return self._parser.parse(tokens, state=self)
