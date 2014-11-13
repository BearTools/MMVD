# coding: utf-8
import numpy as np
import heapq


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
    message = "Couldn't find a route to the destination."


def neighbors(map_, position, available_only=False, positions=True):
    """
    Return Von Neumann neighborhood of distance r=1.

    :param array map_: a warehouse map
    :param pair position: a `(x, y)` of current position on the map
    :param bool available_only: return only available moves (according to the
                                traffic rules)
    :param bool positions: return pairs `(x, y)` instead of values `map_[y][x]`
    """
    x, y = position

    # what's under position in the direction ↑→↓← of the current node
    up, right, down, left = 0, 0, 0, 0
    up_pos, right_pos, down_pos, left_pos = None, None, None, None

    if x - 1 >= 0:
        left = map_[y][x - 1]
        left_pos = (x - 1, y)
    if x + 1 < len(map_[x]):
        right = map_[y][x + 1]
        right_pos = (x + 1, y)
    if y - 1 >= 0:
        up = map_[y - 1][x]
        up_pos = (x, y - 1)
    if y + 1 < len(map_):
        down = map_[y + 1][x]
        down_pos = (x, y + 1)

    results = [[True, up], [True, right], [True, down], [True, left]]

    # rules according to right-hand traffic (suck it, Britain!)
    # 1. can't go in opposite (180°) direction
    # 2. can't turn left
    allowed_moves = {
        1: (1, 2),
        2: (2, 3),
        3: (3, 4),
        4: (4, 1)
    }

    if available_only:
        # set to False these pairs that point in the forbidden direction
        current = map_[y][x]

        if isinstance(current, str):
            # case for shelves
            allowed = list(range(1, 10))  # numbers 1..9
        elif current == 9:
            allowed = list(range(1, 5))
        else:
            # case for roads
            allowed = allowed_moves[current]

        for i in range(4):
            # Only accept outgoing roads, not incoming, so direction
            # index=0 (↑) can't be 3 (↓), index=1 (→) can't be 4 (←), etc.
            # And block not allowed routes, too.
            if (results[i][1] not in allowed or
                    results[i][1] == (i + 2) % 4 + 1):
                results[i][0] = False

    if positions:
        # return positions instead of actual values
        results[0][1] = up_pos
        results[1][1] = right_pos
        results[2][1] = down_pos
        results[3][1] = left_pos

    # return only directions that have True as the first element in pair
    return tuple(map(lambda x: x[1], filter(lambda x: x[0], results)))


def build_path(start, finish, parent):
    """
    Adapted from:
    http://dave.dkjones.org/posts/2012/2012-03-12-astar-python.html
    """
    x = finish
    xs = [x]
    while x != start:
        x = parent[x]
        xs.append(x)
    xs.reverse()
    return xs


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
    Adapted from:
    http://dave.dkjones.org/posts/2012/2012-03-12-astar-python.html
    """
    heap = []

    link = {}  # parent node link
    h = {}  # heuristic function cache
    g = {}  # shortest path to a node

    # keeping track of these numbers in memory for lower footprint
    g[start_position] = 0
    h[start_position] = 0
    link[start_position] = None

    heapq.heappush(heap, (0, 0, start_position))
    # keep a count of the  number of steps, and avoid an infinite loop.
    for step in xrange(1000000):
        f, junk, current = heapq.heappop(heap)

        if current == end_position:
            print "distance:", g[current], "steps:", step
            return g[current], step, build_path(start_position, end_position,
                                                link)

        # get only the neighbors that we can go to
        moves = neighbors(map_, current, available_only=True, positions=True)

        distance = g[current]
        for move in moves:
            if move not in g or g[move] > distance + 1:
                g[move] = distance + 1
                if move not in h:
                    h[move] = heuristic(map_, move, end_position)
                link[move] = current
                heapq.heappush(heap, (g[move] + h[move], -step, move))
    else:
        raise CannotFindPath()
