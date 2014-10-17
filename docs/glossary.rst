Glossary
========

.. glossary::
    :sorted:

    public
        A public API may be used by code which exists in a different
        package. Any API which begins with an underscore is not public.

    persistent
        Persistent data structures are ones which are immutable (they can't be
        changed), but have methods which return "mutations" of themselves. For
        example, a persistent sequence might have an ``append()`` method which
        returns a sequence with that has one more element at the end. These
        typically use structural sharing to lower the cost.

    task failure
        Tasks in Bagel execute independently. When a task crash is triggered,
        that task dies, but other tasks are unaffected. It is possible for
        other tasks to observe that failure if the wish.
