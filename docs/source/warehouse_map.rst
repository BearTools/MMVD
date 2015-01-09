.. _warehouse_map:

Warehouse map
=============

Warehouses are defined in text files.

Textual representation
----------------------

A warehouse map is a text file. Each line represents one row in a map, each
character represents one cell.

+---+---+---+---+---+
| → | → | → | → | ↓ |
+---+---+---+---+---+
| ↑ | a | ↑ | b | ↓ |
+---+---+---+---+---+
| ↑ | c | ↑ | d | ↓ |
+---+---+---+---+---+
| ↑ | e | ↑ | f | ↓ |
+---+---+---+---+---+
| ↑ | ↑ | ← | ← | × |
+---+---+---+---+---+

Each arrow represents a one-way route. Each letter represents a shelf. Cross
(``×``) is a dropzone.

This warehouse is represented in a text form below::

  22223
  1a1b3
  1c1d3
  1e1f3
  14449

So the representation is as follows:

0, 5, 6, 7, 8
  unused

1, 2, 3, 4
  Directions: ↑, →, ↓, ←

9
  a dropzone

a-z, A-Z
  shelves

In-memory representation
------------------------

A map is represented in Python as 2-dimentional array (list of lists), indexed
from 0 and from top-left corner.  For example, on the above map the dropzone
has the position ``(4, 4)``.

Numbers are converted from string character to actual integer value, but
letters (shelves) keep stored as characters.

All positions are indexed in this manner: ``map[Y][X]``.  This is not natural
but it's a convention in Mathematics, computer files and some other places.
For example, to access 2-D matrix elements in Mathematics you first access
row, then column.

Similarily
