.. highlightlang:: python

Warehouse visualization
=======================

New ``visualization.py`` file was introduced to project!

In order to use classes included in ``visualization.py`` one needs:

* :ref:`warehouse map <warehouse_map>`::

    map_ = [
        [2, 2, 2, 2, 3],
        [1, "a", 3, "b", 3],
        [1, "c", 3, "d", 3],
        [1, "e", 3, "f", 3],
        [1, 4, 4, 4, 9],
    ]

* :ref:`list of robots <robots_map>`::

    robots = ((0, 0), (1, 1), (2, 3), (4, 2))

In order to create instance of magazine::

    app = Visualization(map_)

Function introduces robots. Each of robots is given id number starting from 0.
Can be used to introduce all robots at the same time as well as to introduce
any number of robots at the same time::

    app.draw_robots(robots)

In order to run animation one must specify two lists:

* List of all robots positions that are to be updated. List can consist of any
  number of valid robot direction pairs. Robots are accessed by id number
  given to them during draw_robots call. Directions are encoded in standard
  way: 1=up, 2=right, 3=down, 4=left::

    update_robots = [ [0, 2], [1, 2], [2, 3], [3, 3] ]

* List of all shelfs positions that are to be updated. List can consist of any
  number of valid shelf direction pairs. Shelfs are accessed by their name
  form map eg : "a", "b", "c"...  Directions are encoded in standard way:
  1=up, 2=right, 3=down, 4=left

Every shelf can be hidden in that case direction equals to 0::

    update_shelfs = [ ["d", 2] ]

In order to animate, call::

    app.animate(update_robots, update_shelfs)

Animation ends with::

    app.end()
