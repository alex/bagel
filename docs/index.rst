Welcome to Bagel
================

Bagel is a programming language. It's designed to make it easy to build highly
reliable programs, without sacrificing development time. Let's write our first
bagel program, the famous "Hello World" program::

    from std.io import StdIO

    def main(stdio: StdIO) -> ProgramResult:
        stdio.out.write(b"Hello World\n")

Design goals
------------

Bagel is:

* Statically typed
* Statically compiled
* Garbage collected
* Statically linked - The result of compilation is a single, isolated artifact.
* Concurrent and parallel
* Type safe and memory safe
* Fun to use

Bagel is designed for:

* Readability above writeability
* Encouraging testable programs
* Primarily writing network services
* Performance
* Helping you write better programs

Bagel is **not** designed for:

* Interoperability with legacy programming languages
* Being 100% as fast as possible, 95% is fine.

As a result, some of the features Bagel has are:

* Interfaces
* Powerful enums
* Pattern matching
* Compile time reflection and metaprogramming
* Powerful testing tools
* Local type inference

Language features
-----------------

.. toctree::

    features/enums
