import textwrap

from bagel import cfg, parser


def serialize_value(value):
    if isinstance(value, cfg.ConstantInt):
        return str(value._value)
    elif isinstance(value, cfg.LocalName):
        return str(value._name)
    elif isinstance(value, cfg.InstructionResult):
        return "@" + value._name


def serialize_instruction(instruction):
    instruction_string = instruction._opcode.name
    instruction_string += " " + ", ".join(
        serialize_value(v) for v in instruction._arguments
    )
    if instruction._result:
        instruction_string += " -> {}".format(
            serialize_value(instruction._result)
        )
    return instruction_string


def serialize_block(result, block):
    if block._name != "B0":
        result.append("---")
    result.append("{}:".format(block._name))
    for instruction in block._instructions:
        result.append(serialize_instruction(instruction))

    exit = block._exit_condition
    if isinstance(exit, cfg.ReturnValue):
        result.append(":RETURN {}".format(serialize_value(exit._value)))
    elif isinstance(exit, cfg.ConditionalBranch):
        result.append(":CONDITIONAL_BRANCH {}, {}, {}".format(
            serialize_value(exit._condition),
            exit._if_target._name,
            exit._else_target._name
        ))
        serialize_block(result, exit._if_target)
        serialize_block(result, exit._else_target)


def serialize_function(function):
    result = []
    serialize_block(result, function._entry_block)
    return result


def assert_lowers(source, expected_function):
    source = textwrap.dedent(source).lstrip()
    ast = parser.Parser().parse(source)
    namespace = cfg.Namespace()
    cfg.ASTToControlFlowVisitor().visit(ast, namespace)

    serialized_function = serialize_function(namespace.find_function("f"))
    expected_serialization = [
        line.strip()
        for line in expected_function.splitlines()
        if line.strip()
    ]
    assert serialized_function == expected_serialization


class TestCFGLowering(object):
    def test_simple_function(self):
        assert_lowers("""
        def f() -> Int:
            return 3
        """, """
        B0:
        :RETURN 3
        """)

    def test_assignment(self):
        assert_lowers("""
        def f() -> Int:
            a = 3
            return a
        """, """
        B0:
        ASSIGN 3 -> a
        :RETURN a
        """)

    def test_lower_assignment_arithmetic(self):
        assert_lowers("""
        def f() -> Int:
            a = 3
            b = 5
            c = a + b
            return 4 + c
        """, """
        B0:
        ASSIGN 3 -> a
        ASSIGN 5 -> b
        ADD a, b -> @v0
        ASSIGN @v0 -> c
        ADD 4, c -> @v1
        :RETURN @v1
        """)

    def test_if_statement(self):
        assert_lowers("""
        def f():
            a = 4
            if a:
                return 5
            else:
                return 6
        """, """
        B0:
        ASSIGN 4 -> a
        :CONDITIONAL_BRANCH a, B1, B2
        ---
        B1:
        :RETURN 5
        ---
        B2:
        :RETURN 6
        """)
