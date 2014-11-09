Enums
=====

Like many other languages, enums in Bagel let you specify several different
values a variable can contain::

    enum type MeasuringSystem:
        case Imperial
        case Metric

We use the ``case`` keyword to indicate each possible value an ``enum`` can
contain.

Then we can declare functions which take one of these values, and use
pattern matching to handle them::

    def distance_unit(system: MeasuringSystem) -> Text:
        match system:
            with MeasuringSystem.Imperial:
                return "Feet"
            with MeasuringSystem.Metric:
                return "Meters"

The Bagel compiler will make sure that you handle all possible cases, so if you
add a new value to ``MeasuringSystem`` without adding handling to
``distance_unit`` you will get a compilation error, telling you about the
unhandled case.

Unlike many programming languages, Bagel's enums can contain other values::

    enum type Distance:
        case Inches(UInt)
        case Feet(UInt)

Again, we can use pattern matching to handle these, also unpacking the values::

    def distance_in_inches(d: Distance) -> UInt:
        match d:
            with Distance.Inches(x):
                return x
            with Distance.Feet(x):
                return x * 12

Enum values are immutable, after creating one, it's not possible to change any
of the values inside of it.

You can make use of both of these features in a single enum. When an enum
contains another value, it can optionally be given a label::

    enum type TalkSubmissionStatus:
        case Accepted
        case InReview
        case Rejected(reason: Text)


    def talk_status_notice(status: TalkSubmissionStatus) -> Text:
        match status:
            with TalkSubmissionStatus.Accepted:
                return "Your talk was accepted"
            with TalkSubmissionStatus.InReview:
                return "Your talk is still being reviewed"
            with TalkSubmissionStatus.Rejected(reason):
                return reason
