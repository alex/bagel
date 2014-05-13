Interfaces
==========

::

    interface class TestResult:
        def print_result(self, w: io.Writer)

    class TestPassed:
        def print_result(self, w: io.Writer):
            w.write(b"PASSED\n")

    class TestFailure:
        def print_result(self, w: io.Writer):
            w.write(b"FAILURE\n")

    def test_finished(stdout: io.Writer, t: TestResult):
        t.print_result(stdout)
