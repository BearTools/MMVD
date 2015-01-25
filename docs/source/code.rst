.. code:

Code documentation
==================

The project is divided into Python application (mmvdApp), tests, and
documentation.

In this part we cover our code documentation.

Main module
-----------

.. automodule:: mmvdApp.main
  :members:


Visualization module
--------------------

.. automodule:: mmvdApp.visualization
  :members:

Charts generating module
------------------------

.. automodule:: mmvdApp.charts
  :members:

Pathing module
--------------

.. automodule:: mmvdApp.shortest_path
  :members:

  .. autofunction:: mmvdApp.shortest_path.a_star(map_, start_position, end_position, only_distance=False)

Utils package
-------------

``mmvdApp.utils`` consists of some auxiliary modules.

IO module
~~~~~~~~~

.. automodule:: mmvdApp.utils.io
  :members:

Linear programming module
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mmvdApp.utils.linprog
  :members:

  .. autofunction:: mmvdApp.utils.linprog.valid_solution(solution, order, dropzone)

Map helpers
~~~~~~~~~~~

.. automodule:: mmvdApp.utils.map
  :members:

Memoization decorator
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mmvdApp.utils.memoization
  :members:

Tabu search module
~~~~~~~~~~~~~~~~~~

.. automodule:: mmvdApp.utils.tabu
  :members:
