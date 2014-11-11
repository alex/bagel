from rply import ParserGenerator

from bagel import ast, lexer


class Parser(object):
    _pg = ParserGenerator([
        "NEWLINE", "INDENT", "DEDENT",

        "ARROW", "COLON", "COMMA", "EQUAL",

        "PLUS",

        "LPAREN", "RPAREN",

        "CASE", "CLASS", "DEF", "ENUM", "MATCH", "RETURN", "TYPE", "WITH",

        "NAME", "INTEGER",
    ], precedence=[
        ("left", ["PLUS"]),
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
    @_pg.production("declaration : enum_case")
    def declaration(self, p):
        return p[0]

    @_pg.production("function : DEF NAME LPAREN RPAREN return_type COLON"
                    "           NEWLINE INDENT suite DEDENT")
    def function(self, p):
        return ast.Function(
            p[1].getstr(), [], p[4], p[8],
        )

    @_pg.production("return_type : none")
    def function_return_type_none(self, p):
        return p[0]

    @_pg.production("return_type : ARROW expression")
    def function_return_type_arrow_expression(self, p):
        return p[1]

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

    @_pg.production("enum_case : CASE NAME NEWLINE")
    def case_name(self, p):
        return ast.EnumCase(p[1].getstr())

    @_pg.production("enum_case : CASE NAME LPAREN enum_case_members RPAREN "
                    "            NEWLINE")
    def case_call(self, p):
        return ast.EnumCase(p[1].getstr(), p[3])

    @_pg.production("enum_case_members : expression")
    def case_members_case_member(self, p):
        return [p[0]]

    @_pg.production("enum_case_members : enum_case_members COMMA expression")
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

    @_pg.production("statement : return")
    @_pg.production("statement : assignment")
    @_pg.production("statement : match")
    @_pg.production("statement : expression NEWLINE")
    def statement(self, p):
        return p[0]

    @_pg.production("return : RETURN expression NEWLINE")
    def statement_return_expression_newline(self, p):
        return ast.Return(p[1])

    @_pg.production("assignment : expression EQUAL expression NEWLINE")
    def assignment_expression_equal_expression(self, p):
        return ast.Assignment(p[0], p[2])

    @_pg.production("match : MATCH expression COLON NEWLINE INDENT "
                    "        match_case match_cases DEDENT")
    def statement_match(self, p):
        return ast.Match(p[1], [p[5]] + p[6])

    @_pg.production("match_cases : none")
    def match_cases(self, p):
        return []

    @_pg.production("match_cases : match_cases match_case")
    def match_cases_match_cases_match_case(self, p):
        return p[0] + [p[1]]

    @_pg.production("match_case : WITH expression COLON NEWLINE INDENT suite "
                    "             DEDENT")
    def match_case(self, p):
        return ast.MatchCase(p[1], p[5])

    @_pg.production("expression : binop")
    @_pg.production("expression : atom")
    def expression(self, p):
        return p[0]

    @_pg.production("binop : expression PLUS expression")
    def binop(self, p):
        return ast.BinOp(p[1].getstr(), p[0], p[2])

    @_pg.production("atom : INTEGER")
    def atom_integer(self, p):
        return ast.Integer(int(p[0].getstr()))

    @_pg.production("atom : NAME")
    def atom_name(self, p):
        return ast.Name(p[0].getstr())

    @_pg.production("none : ")
    def none(self, p):
        return None

    _parser = _pg.build()

    def parse(self, source):
        tokens = lexer.Lexer().lex(source)
        return self._parser.parse(tokens, state=self)
