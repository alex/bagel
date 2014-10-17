Classes
=======

Bagel is an object-oriented programming language, in the sense that you can
define classes and associate data and functions with them. However, unlike many
other object-oriented languages, in Bagel there is no inheritance::

    class type Point:
        x: Int
        y: Int
        z: Int

Here we've defined a class, ``Point``, with three fields, ``x``, ``y``, and
``z``, all of which are ``Ints``. Classes with all :term:`public` fields get a
public constructor, so we can easily create a point instance::

    p = Point(x=1, y=2, z=3)

We can define methods on our ``Point`` class::

    class type Point:
        # ...

        def translate(self, dx: Int, dy: Int, dz: Int) -> Point:
            return Point(self.x + dx, self.y + dy, self.z + dz)

Then we can easily call these this method::

    new_p = p.translate(-1, -1, 0)

Fields on an object cannot be modified after it's created, meaning code like::

    p.x = 2

Causes a compilation error.

If you want your class to have a constructor other than the default one, you
can achieve this by adding a class method::

    class type Point:
        x: Int
        y: Int
        z: Int

        classdef new(x: Int, y: Int, z=0: Int) -> Point:
            return Point(x=x, y=y, z=z)

Now we can create point instances with or without the ``z`` argument::

    p = Point.new(2, 3)
