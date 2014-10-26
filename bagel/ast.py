class Module(object):
    def __init__(self, declarations):
        self._declarations = declarations

    def visit(self, visitor, arg):
        return visitor.visit_module(self, arg)


class Class(object):
    def __init__(self, name, declarations):
        self._name = name
        self._declarations = declarations

    def visit(self, visitor, arg):
        return visitor.visit_class(self, arg)


class Enum(object):
    def __init__(self, name, cases):
        self._name = name
        self._cases = cases

    def visit(self, visitor, arg):
        return visitor.visit_enum(self, arg)


class EnumCase(object):
    def __init__(self, name, members=None):
        self._name = name
        self._members = members

    def visit(self, visitor, arg):
        return visitor.visit_enum_case(self, arg)


class Attribute(object):
    def __init__(self, name, tp):
        self._name = name
        self._tp = tp

    def visit(self, visitor, arg):
        return visitor.visit_attribute(self, arg)


class Function(object):
    def __init__(self, name, arguments, return_type, body):
        self._name = name
        self._arguments = arguments
        self._return_type = return_type
        self._body = body

    def visit(self, visitor, arg):
        return visitor.visit_function(self, arg)


class Return(object):
    def __init__(self, value):
        self._value = value

    def visit(self, visitor, arg):
        return visitor.visit_return(self, arg)


class Suite(object):
    def __init__(self, body):
        self._body = body

    def visit(self, visitor, arg):
        return visitor.visit_suite(self, arg)


class Name(object):
    def __init__(self, value):
        self._value = value

    def visit(self, visitor, arg):
        return visitor.visit_name(self, arg)


class Integer(object):
    def __init__(self, value):
        self._value = value

    def visit(self, visitor, arg):
        return visitor.visit_integer(self, arg)
