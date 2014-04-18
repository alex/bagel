Welcome to Bagel
================

Bagel is a programming language. It's designed to make it easy to build highly
reliable programs, without sacrificing development time. Let's write our first
bagel program, the famous "Hello World" program::

    from std.io import StdIO

    def main(stdio: StdIO) -> ProgramResult:
        stdio.out.write(b"Hello World\n")
