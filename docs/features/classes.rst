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
default constructor, so we can easily create a point instance::

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

Now we can do::

    p = Point(x=1, y=2)
    p.x = 5

If you want your class to have a constructor other than the default one, you
can achieve this by adding an ``__new__`` method::

    class Point:
        x: Int
        y: Int
        z: Int

        def __new__(x: Int, y: Int, z=0: Int) -> Point:
            return new(Point, x=x, y=y, z=z)

Now we can create point instances with or without the ``z`` argument. The
``__new__`` function is invoked when we call ``Point()``. The ``new()``
function takes a class, and invokes the default constructor, returning a new
instance of the class.
