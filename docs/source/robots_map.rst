.. _robots_map:

Robot positions
===============

Robot positions are read from a text-file on user's disk.

Textual representation
----------------------

A robots positions file is a text file with stored starting positions for
every robot in the warehouse.  Number of non-empty lines dictates number of
robots. Each line represents one robot starting position in the format ``Y,X``
(or ``row,column``).

Robots can all start from the same position.

For the example map below:

+---+---+---+---+---+
| → | → | → | → | ↓ |
+---+---+---+---+---+
| ↑ | o | ↑ | o | ↓ |
+---+---+---+---+---+
| ↑ | o | ↑ | o | ↓ |
+---+---+---+---+---+
| ↑ | o | ↑ | o | ↓ |
+---+---+---+---+---+
| ↑ | ↑ | ← | ← | × |
+---+---+---+---+---+

you can define 3 robots all starting in the bottom-right corner of the map::

    4,4
    4,4
    4,4

In-memory representation
------------------------

Utility function :py:func:`mmvdApp.utils.io.read_robots_positions` reads a file
with starting positions and returns them as a list of pairs::

    [(4, 4), (4, 4), (4, 4)]
