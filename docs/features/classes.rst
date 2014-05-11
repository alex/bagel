Classes
=======

Bagel is an object-oriented programming language, in the sense that you can
define classes and assosciate data and functions with them::

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
