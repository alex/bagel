Packaging and Build System
==========================

Running a Bagel program is a single command:

.. code-block:: console

    $ bagel run hello.bagel
    Hello World

Building an executable is also a single command:

.. code-block:: console

    $ bagel build hello.bagel
    $ ./hello
    Hello World

The resulting binary is completely stand-alone, it has no external dependencies
and can be run on any machine, as long as it has the same operating system and
CPU architecture as the machine it was compiled on.

To use a third-party package in your Bagel program, you can create a
``hello.bagel-conf`` and specify the needed packages:

.. code-block:: yaml

    package:
        dependencies:
            - cream_cheese
            - lox

Now when you run ``bagel run`` or ``bagel build``, the compiler will
automatically fetch the ``cream_cheese`` and ``lox`` packages from the central
``bagel`` package repository.

Now your code will be able to import things from these libraries::

    import cream_cheese.Schmear

You can also install packages from a version control system:

.. code-block:: yaml

    package:
        dependencies:
            - name: lox
              repository: git://github.com/alex/lox

Internal Dependencies
---------------------

One common issue that arises with packaging is multiple dependencies, which
require different versions of the same package. To solve this, Bagel allows a
package to define internal dependencies. A package's internal dependencies are
allowed to have version conflicts with other package's dependencies. The only
limitation is that no part of the :term:`public` API may use something from
this package.

.. code-block:: yaml

    package:
        dependencies:
            # Everything in the system must use the 1.0 version of
            # cream_cheese.
            - cream_cheese==1.0

        internal-dependencies:
            # Other packages may use other versions of lox.
            - lox==1.2

Alternate package repositories
------------------------------

By default, ``bagel`` will fetch all of your dependencies from the central
``bagel`` package repository. However, packages can also specify other
locations to get packages from, either in addition to the default servers, or
in stead of. This can be used to either set up a local mirror, or to host non-
public packages:

.. code-block:: yaml

    package-indexes:
        # This is the default root server, you can provide your own!
        root-index: packages.bagel.bagel
        # These servers will also be checked.
        additional-indexes:
            - bagel-packages.my-company.com

.. note::

    Be aware, the ``package-indexes`` value will only be respected in the root
    ``.bagel-conf`` file. Dependencies cannot specify additional locations to
    find packages, this is to prevent a dependency from forcing you to get
    packages from a different location.
