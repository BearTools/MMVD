Testing
=======

To test you need `py.test <http://pytest.org/latest/>`_ testing suite.

Running tests is as easy as invoking::

    $ py.test

Tests are marked as either ``utils`` (for testing utility functions or
classes)  or ``frontend`` (for testing Tk GUI).  You can select specific tests
to run with this command::

    $ py.test -m utils

To see all available markers (works only with built-in markers)::

    $ py.test --markers
