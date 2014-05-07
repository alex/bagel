Enums
=====

Like many other languages, enums in Bagel let you specify several different
values a variable can contain::

    enum class MeasuringSystem:
        Imperial
        Metric

Then we can declare functions which take one of these values, and use
:term:`pattern matching` to handle them::

    def distance_unit(system: MeasuringSystem) -> Text:
        match system:
            as Imperial:
                return "Feet"
            as Metric:
                return "Meters"

The Bagel compiler will make sure that you handle all possible cases, so if you
add a new value to ``MeasuringSystem`` without adding handling to
``distance_unit`` you will get a compilation error, tell you about the
unhandled case.

Unlike many programming languages, Bagel's enums can contain other values::

    enum class Distance
        Inches(UInt)
        Feet(UInt)

Again, we can use pattern matching to handle these values, also unpacking the
value::

    def distance_in_inches(d: Distance) -> UInt:
        match d:
            as Inches(x):
                return x
            as Feet(x):
                return x * 12

Enum values are immutable, after creating one, it's not possible to change any
of the values inside of it.
