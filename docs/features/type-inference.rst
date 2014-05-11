Local type inference
====================

Bagel is a statically typed language, meaning at compile-time, it's possible to
know what type every variable has. Like in many other statically compiled
languages, this means that program authors need to explicitly state a
function's arguments' types as well as return value::

    def f(x: Int) -> Int:
        # ...

Here ``f`` is a function which takes a single argument, ``x``, which is an
``Int``. It returns an ``Int``. Unlike in many other statically typed
languages, in Bagel it is not necessary to specify the types of local
variables::

    def sum(x: Int, y: Iny, z: Int) -> Int:
        partial_sum = x + y
        full_sum = partial_sum + z
        return full_sum

Here the compiler is able to automatically *infer* that ``partial_sum`` and
``full_sum`` are both ``Ints``.
