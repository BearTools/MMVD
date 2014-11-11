# coding: utf-8
import numpy as np


def read_warehouse_map(name, use_numpy=False):
    """
    Read the file line by line and represent it as an array or list of lists.
    """
    with open(name, 'r') as f:
        lines = f.readlines()
    lines = map(lambda x: x.rstrip(), lines)  # get rid of line endings
    lines = filter(len, lines)  # get rid of empty lines
    lines = map(list, lines)  # split each line into list (ie. mutable string)

    # change '0' to '9' into integers 0-9
    for k1, v1 in enumerate(lines):
        for k2, v2 in enumerate(v1):
            try:
                v2_ = int(v2)
            except ValueError:
                v2_ = v2
            lines[k1][k2] = v2_

    if use_numpy:
        # CAUTION: Numpy arrays don't support mixed ints and chars, there's
        #          gonna be all characters.
        lines = np.array(lines)

    return lines


class CannotFindPath(Exception):
    """
    Path-finding algorithm raises this exception in case of failure in finding
    path to the destination.
    """
    pass


def neighbor(map_, position):
    """
    Return Von Neumann neighborhood of distance r=1.  In case of going out
    of range, return 0 (empty cell).
    """
    x, y = position
    up, right, down, left = 0, 0, 0, 0

    if x - 1 >= 0:
        left = map_[y][x - 1]
    if x + 1 < len(map_[x]):
        right = map_[y][x + 1]
    if y - 1 >= 0:
        up = map_[y - 1][x]
    if y + 1 < len(map_):
        down = map_[y + 1][x]

    return up, right, down, left


def heuristic(map_, start_position, end_position):
    """
    A helper heuristic function.
    Return value indicating cost of going from start_position to end_position.
    """
    x1, y1 = start_position
    x2, y2 = end_position
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def shortest_path(map_, start_position, end_position):
    """
    Find shortest path from ``start_position`` to ``end_position`` on the
    ``map_``.
    """
    UP, RIGHT, DOWN, LEFT = 1, 2, 3, 4
    # Steps:
    # 1. Find closest road.  If there's more than one, use the best one
    #    according to heuristic function.
    # 2. Follow roads to the destination (help yourself using heuristic
    #    function).
    pass
