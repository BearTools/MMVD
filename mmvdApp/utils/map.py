# coding: utf-8

from collections import OrderedDict
from ..shortest_path import a_star


def drop_zone(map):
    """
    Find the drop zone coordinates.

    :param array map: a warehouse map
    :return: coordinates of the drop zone
    :rtype: pair ``(y, x)``
    """
    dz = (-1, -1)

    # TODO: can optimize by breaking the loop
    for row_index, row in enumerate(map):
        for column_index, point in enumerate(row):
            if point == 9 or point == "9":
                dz = (row_index, column_index)

    return dz


def products(map, order):
    """
    Find coordinates for each product in order.

    :param array map: a warehouse map
    :param list order: a specific sequence of products
    :return: coordinates for products in the same sequence as they are
             specified in ``order``
    :rtype: list of pairs ``(y, x)``
    """
    # CAUTION:
    # Make sure to return coordinates in the same order as corresponding
    # products in `order`.
    # OrderedDict from `collections` is perfect for this job.

    # if, for example, order == ['d', 'a', 'f']
    # then rv == {'d': None, 'a': None, 'f': None}
    rv = OrderedDict.fromkeys(order)

    for row_index, row in enumerate(map):
        for column_index, point in enumerate(row):
            # if the point is str and in `order`, then we should save it's
            # coordinates
            if isinstance(point, str) and point in order:
                # save coords
                rv[point] = (row_index, column_index)

    return rv.values()


def distances(map, points, start_pos, end_pos):
    """
    For all points, calculate distance from starting point, to this point, to
    ending point.
    Distances are calculated using A* algorithm implemented with traffic rules.

    :param array map: a warehouse map
    :param list points: a list of tuples with 2 elements:
                        ``[(0, 1), (1, 1), ...]``
    :param tuple start_pos: tuple with route beginning point: ``(y, x)``
    :param tuple end_pos: tuple with route beginning point: ``(y, x)``
    :rtype: list of pairs
    :return: list of tuples with distances from parameter ``start_pos`` to each
             point and from each point to parameter ``end_pos``
    """
    d = []
    for point in points:
        distance_to = a_star(map, start_pos, point, only_distance=True)
        distance_from = a_star(map, point, end_pos, only_distance=True)
        d.append((distance_to, distance_from))

    return d
