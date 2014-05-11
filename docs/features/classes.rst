Classes
=======

Bagel is an object-oriented programming language, in the sense that you can
define classes and assosciate data and functions with them. However, unlike
many other object-oriented languages, in Bagel there is no inheritance::

    class Point:
        x: Int
        y: Int
        z: Int

Here we've defined a class, ``Point``, with three fields, ``x``, ``y``, and
``z``, all of which are ``Ints``. Classes with all :term:`public` fields get a
default constrcutor, so we can easily create a point instance::

    p = Point(x=1, y=2, z=3)

We can define methods on our ``Point`` class::

    class Point:
        # ...

        def translate(self, dx: Int, dy: Int, dz: Int) -> Point:
            return Point(self.x + dx, self.y + dy, self.z + dz)

Then we can easily call these this method::

    new_p = p.translate(-1, -1, 0)

By default, all fields on a class are immutable, meaning code like::

    p.x = 2

Causes a compilation error. If we want to create a mutable ``Point``, we can
add the ``mutable`` keyword to the field definitions::

    class Point:
        mutable x: Int
        mutable y: Int

Now::

    p = Point(x=1, y=2)
    p.x = 5

Works.
