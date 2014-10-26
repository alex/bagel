class Module(object):
    def __init__(self, declarations):
        self._declarations = declarations

    def __eq__(self, other):
        return self._declarations == other._declarations


class Function(object):
    def __init__(self, name, arguments, return_type, body):
        self._name = name
        self._arguments = arguments
        self._return_type = return_type
        self._body = body

    def __eq__(self, other):
        return (
            self._name == other._name and
            self._arguments == other._arguments and
            self._return_type == other._return_type and
            self._body == other._body
        )


class Return(object):
    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        return self._value == other._value


class Suite(object):
    def __init__(self, body):
        self._body = body

    def __eq__(self, other):
        return self._body == other._body


class Integer(object):
    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        return self._value == other._value
