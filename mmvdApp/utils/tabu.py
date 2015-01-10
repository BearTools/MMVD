# coding: utf-8
import itertools


def initial_solution(robots, order):
    """
    Provide initial solution to tabu search algorithm.

    Take all robots, for example ``[0, 1, 2, 3]``, and arrange them to products
    in ``order``.

    This arranges robots in a cyclic manner.  If there are twice as many
    products, as there are robots, then arrangement goes like:
    ``[0, 1, 2, 3, 0, 1, 2, 3]``.

    :param list robots: list of robot indices, for example: ``[0, 1, 2, 3]``
    :param list order: a specific sequence of products
    :return: arrangement (robots → products) made from ``robots``
    """
    generator = itertools.cycle(robots)
    arrangement = []
    for i in range(len(order)):
        arrangement.append(next(generator))
    return arrangement


def tabu_search(map, robots, order, product_distances):
    """
    Compute best (not necessarily optimal) arrangement (robots → products),
    that is both valid (see :func:`mmvdApp.utils.linprog.valid_solution`) and
    has lowest available cost (see
    :func:`mmvdApp.utils.linprog.objective_function`).

    Computation is done using
    `Tabu search algorithm <http://en.wikipedia.org/wiki/Tabu_search>`_.

    :param array map: a warehouse map
    :param list robots: list of indices, for example: ``[0, 1, 2, 3]``.  This
                        means there are 4 robots that start from the drop zone
                        in this particular order.
    :param list order: a specific sequence of products that have to be dropped
                       in the dropzone in this specific order
    :param list product_distances: a helper list of distance tuples
                                   ``(to, from)`` the product on the map.
                                   Starting point is always dropzone, so is
                                   ending point.
    :return: a pair, ``result`` and ``solution``.  ``result`` carries best
             objective function value.  ``solution`` provides valid solution
             steps (as stated by :func:`mmvdApp.utils.linprog.valid_solution`
             function).
    """
    result = None
    solution = []
    return result, solution
