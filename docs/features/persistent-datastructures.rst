Persistent Data Structures
==========================

Bagel includes several :term:`collection` data types, which are homogenous
groupings of multiple other values. All of Bagel's builtin collections are
:term:`persistent`, which means their contents can't be changed, but they do
have operations for getting a copy of themselves some changes.

The simplest of Bagel's datastructures is the ``List``, they have a builtin
syntax for creation::

    l = [1, 2, 3, 4]

Now we have a ``List``, ``l``, with 4 elements. All of a List's elements must
be the same type, the following is an error::

    l = [1, "abc", []]

To add a number to our list, we can use the ``append`` method::

    new_l = l.append(5)

Now ``new_l`` is ``[1, 2, 3, 4, 5]``. ``l`` was not modified, it's still
``[1, 2, 3, 4]``.

As in many languages, we can index into a ``List`` to get a value at a specific
point::

    x = l[3]

Now ``x`` is equal to 4.

If you index past the end of a ``List`` a :term:`task failure` will be
triggered, stopping the execution of the current task.
