from rply import ParserGenerator

from bagel import ast, lexer


class Parser(object):
    _pg = ParserGenerator([
        "NEWLINE", "INDENT", "DEDENT",

        "COLON", "COMMA",

        "LPAREN", "RPAREN",

        "CASE", "CLASS", "DEF", "ENUM", "RETURN", "TYPE",

        "NAME", "INTEGER",
    ])

    @_pg.production("program : module")
    def program_module(self, p):
        return p[0]

    @_pg.production("module : declarations")
    def module_declarations(self, p):
        return ast.Module(p[0])

    @_pg.production("declarations : none")
    def declarations_none(self, p):
        return []

    @_pg.production("declarations : declarations declaration")
    def declarations_declarations_declaration(self, p):
        return p[0] + [p[1]]

    @_pg.production("declaration : function")
    @_pg.production("declaration : class")
    @_pg.production("declaration : enum")
    @_pg.production("declaration : attribute")
    @_pg.production("declaration : case")
    def declaration(self, p):
        return p[0]

    @_pg.production("function : DEF NAME LPAREN RPAREN COLON NEWLINE INDENT "
                    "           suite DEDENT")
    def function(self, p):
        return ast.Function(
            p[1].getstr(), [], None, p[7],
        )

    @_pg.production("class : CLASS TYPE NAME COLON NEWLINE INDENT declarations"
                    "        DEDENT")
    def class_(self, p):
        return ast.Class(p[2].getstr(), p[6])

    @_pg.production("enum : ENUM TYPE NAME COLON NEWLINE INDENT declarations "
                    "       DEDENT")
    def enum(self, p):
        return ast.Enum(p[2].getstr(), p[6])

    @_pg.production("attribute : NAME COLON expression NEWLINE")
    def attribute(self, p):
        return ast.Attribute(p[0].getstr(), p[2])

    @_pg.production("case : CASE NAME NEWLINE")
    def case_name(self, p):
        return ast.EnumCase(p[1].getstr())

    @_pg.production("case : CASE NAME LPAREN case_members RPAREN NEWLINE")
    def case_call(self, p):
        return ast.EnumCase(p[1].getstr(), p[3])

    @_pg.production("case_members : expression")
    def case_members_case_member(self, p):
        return [p[0]]

    @_pg.production("case_members : case_members COMMA expression")
    def case_members_case_members(self, p):
        return p[0] + [p[2]]

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

    @_pg.production("expression : NAME")
    def expression_name(self, p):
        return ast.Name(p[0].getstr())

    @_pg.production("none : ")
    def none(self, p):
        return None

    _parser = _pg.build()

    def parse(self, source):
        tokens = lexer.Lexer().lex(source)
        return self._parser.parse(tokens, state=self)
