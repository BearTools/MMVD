============================================
MMVD: a robot controlled warehouse simulator
============================================

This application is a real-life example of operational research algorithms
implementation.

A warehouse with robots looks like `this <https://www.youtube.com/watch?v=lWsMdN7HMuA>`__.

There's a number of challenges we have to face when we want to optimize
the workflow in such warehouse.

Challenges
----------

1. Pathfinding (robots should reach shelves in an optimal way, for example:
   cost and time efficient).

2. Managing a fleet of devices (which robots go to charging station, which
   robots pick up specific shelves, etc).

3. Specifying an appearance order for shelves.

This example can be far more advanced, and implementation specific.

Algorithms
----------

We use `A* <http://en.wikipedia.org/wiki/A*_search_algorithm>`_ for finding
paths and `Tabu search <http://en.wikipedia.org/wiki/Tabu_search>`_ for
assigning robots to shelves.

Installation
------------

1. (Optional) Make a virtual environment and activate it::

    $ virtualenv MMVD_venv
    $ source MMVD_venv/bin/activate

2. Clone this repository::

    $ cd MMVD_venv
    $ git clone https://github.com/WojciechFocus/MMVD.git
    $ cd MMVD

3. Install this application::

    $ python setup.py install

It should now be installed.

Development
-----------

Follow :ref:`Installation` but in point 3. invoke this command::

    $ pip install -e .


Launch
------

Not yet.
