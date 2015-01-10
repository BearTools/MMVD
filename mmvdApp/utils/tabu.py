# coding: utf-8
import itertools
import Queue
import heapq

from .linprog import objective_function, valid_solution
from .map import drop_zone
from ..shortest_path import a_star


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
    :rtype: list
    """
    generator = itertools.cycle(robots)
    arrangement = []
    for i in range(len(order)):
        arrangement.append(next(generator))
    return arrangement


# TODO: implement with memoize decorator?
def generate_solution(map, robot_positions, product_positions, order, dropzone,
                      assignment):
    """
    Generate solution steps (states) that form a valid solution (see
    :func:`mmvdApp.utils.linprog.valid_solution`).

    :param array map:
    :param robot_positions:
    :param product_positions:
    :param order:
    :param dropzone:
    :param assignment:
    :return:
    :rtype:
    """
    # for each robot at each starting position generate route to the assigned
    # product
    for product_index, robot_index in enumerate(assignment):
        # product_positions - the same order as in `order`
        distance1, _, route1 = a_star(map, robot_positions[robot_index],
                                      product_positions[product_index])
        distance2, _, route2 = a_star(map, product_positions[product_index],
                                      dropzone)


def neighborhoods(solution):
    """
    Generate neighborhoods for given solution.

    :param list solution: arrangement (robots → products)
    :return: possible permutations of current solution
    :rtype: list
    """
    # TODO: come up with some neighborhoods
    return [solution]


def best_candidate(candidates, order, dropzone):
    """
    Select the best (robots → products) arrangement from all candidates.
    :func:`mmvdApp.utils.linprog.objective_function` provides a way to measure
    "fitness" of given arrangement.

    :param candidates: robot indices.  For example, a candidate ``[1, 2, 0]``
                       means "robot #1 should fetch product #0, robot #2 should
                       fetch product #1, robot #0 should fetch product #2".
    :type candidates: list of candidates
    :param list order: a specific sequence of products that have to be dropped
                       in the dropzone in this specific order
    :param tuple dropzone: coordinates of the drop zone
    :return: lowest objective function value, corresponding candidate and
             generated solution steps
    :rtype: tuple
    """
    rv = []
    for candidate in candidates:
        solution = generate_solution(candidate, order)
        if valid_solution(solution, order, dropzone):
            objective = objective_function(solution)
            heapq.heappush(rv, (objective, candidate, solution))
    return heapq.heappop(rv)


def features(previous, current):
    """
    Compare previous solution and current solution and come up with
    "changes vector".

    :param previous: previous solution
    :param current: current solution
    :return: list with ``None`` on positions where both solutions match, and
             ``current[i]`` on positions where they don't match.
    """
    rv = []
    for x1, x2 in zip(previous, current):
        if x1 == x2:
            rv.append(None)
        else:
            rv.append(x2)
    return rv


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
    MAX_ITERATIONS = 10**3
    MAX_TABU_SIZE = 5

    solution = initial_solution(robots, order)
    best_solution = solution[:]  # copy of solution

    result = objective_function(solution)
    best_result = result

    tabu_list = Queue.Queue(maxsize=MAX_TABU_SIZE)

    dropzone = drop_zone(map)

    i = 0
    while i < MAX_ITERATIONS:
        i += 1

        candidates = []
        for candidate in neighborhoods(best_solution):
            if features(best_solution, candidate) not in tabu_list:
                candidates.append(candidate)

        # best_candidate returns (result, candidate, solution_steps) tuple, but
        # we're not interested in the last one
        result, solution, _ = best_candidate(candidates, order, dropzone)
        if result < best_result:
            previous_solution = best_solution[:]
            best_solution = solution[:]
            best_result = result

            if tabu_list.full():
                tabu_list.get_nowait()

            tabu_list.put_nowait(features(previous_solution, solution))

    return best_result, best_solution
