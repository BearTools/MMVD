# coding: utf-8
import heapq
# from .memoize import memoize  # it's so shitty!


class PathUnreachable(Exception):
    """
    Path-finding algorithm raises this exception in case of failure in finding
    path to the destination.
    """
    message = "Cannot find route to the destination."


def neighbors(map_, position, final=None, available_only=False,
              positions=True):
    """
    Return Von Neumann neighborhood of distance r=1.

    :param array map_: a warehouse map
    :param pair position: a ``(x, y)`` of current position on the map
    :param pair final: a ``(x, y)`` of final position on the map.  If this is
                       specified, and final position is one of the neighbors,
                       it gets included in the results
    :param bool available_only: return only available moves (according to the
                                traffic rules)
    :param bool positions: return pairs ``(x, y)`` instead of values
                           ``map_[y][x]``
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

    # below this point: implementation of right-hand traffic rules

    # import string
    # shelves = tuple(string.ascii_letters)
    # rules according to right-hand traffic (suck it, Britain!)
    # 1. can't go in opposite (180°) direction
    # 2. can't turn left
    allowed_moves = {
        1: (1, 2, 9),
        2: (2, 3, 9),
        3: (3, 4, 9),
        4: (4, 1, 9)
    }

    # checking if neighbors comply with traffic rules
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

    # check if final position is in the closest neighborhood and it's a shelf
    if (positions and final and manhattan_dist(map_, position, final) == 1
            and isinstance(map_[final[1]][final[0]], str)):
        # ...and include it if so
        if final == up_pos:
            results[0][0] = True
        if final == right_pos:
            results[1][0] = True
        if final == down_pos:
            results[2][0] = True
        if final == left_pos:
            results[3][0] = True

    # return only directions that have True as the first element in pair
    return tuple(map(lambda x: x[1], filter(lambda x: x[0], results)))


def manhattan_dist(map_, start_position, end_position):
    """
    Compute Manhattan distance between two points on the same map.
    Return value indicating cost of going from start_position to end_position.

    :param array map_: a warehouse map
    :param pair start_position: a ``(x, y)`` of current position on the map
    :param pair end_position: a ``(x, y)`` of final position on the map
    :return: Manhattan distance between ``start_position`` and ``end_position``
    :rtype: int
    """
    x1, y1 = start_position
    x2, y2 = end_position
    return abs(x1 - x2) + abs(y1 - y2)


def build_path(start, finish, parent):
    """
    Contruct a route from A* algorithms "backwards".

    Adapted from:
    http://dave.dkjones.org/posts/2012/2012-03-12-astar-python.html

    :param pair start: a ``(x, y)`` of starting position on the map
    :param pair finish: a ``(x, y)`` of finish position on the map
    :param dict parent: a dictionary full of node=>parent mappings
    :return: chronological list of visited nodes, e.g.
             ``[(0, 0), (0, 1), ..., (2, 4)]``
    """
    x = finish
    xs = [x]
    while x != start:
        x = parent[x]
        xs.append(x)
    xs.reverse()
    return xs


def a_star(map_, start_position, end_position):
    """
    Find shortest path from ``start_position`` to ``end_position`` on the
    ``map_`` using A* (http://en.wikipedia.org/wiki/A*) algorithm.

    Adapted from:
    http://dave.dkjones.org/posts/2012/2012-03-12-astar-python.html

    :param array map_: warehouse map
    :param pair start_position: a ``(x, y)`` of current position on the map
    :param pair end_position: a ``(x, y)`` of final position on the map
    :return: distance, iteration steps and actual path to the destination
    :raises PathUnreachable: if the algorithm is not able to find a path to the
                             destination
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
        if len(heap) == 0:
            raise PathUnreachable()

        f, junk, current = heapq.heappop(heap)

        if current == end_position:
            print "Distance: {}, steps: {}".format(g[current], step)
            return g[current], step, build_path(start_position, end_position,
                                                link)

        # get only the neighbors that we can go to
        moves = neighbors(map_, current, final=end_position,
                          available_only=True, positions=True)

        distance = g[current]
        for move in moves:
            if move not in g or g[move] > distance + 1:
                g[move] = distance + 1
                if move not in h:
                    h[move] = manhattan_dist(map_, move, end_position)
                link[move] = current
                heapq.heappush(heap, (g[move] + h[move], -step, move))
    else:
        raise PathUnreachable()
