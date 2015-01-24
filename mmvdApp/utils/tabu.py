# coding: utf-8
import itertools
import collections
import heapq
import random

from .linprog import objective_function, valid_solution
from .linprog import RobotCollisionException, InvalidOrderException
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


# TODO: split this into multiple smaller functions?
def generate_solution(map_, robot_positions, product_positions, order,
                      dropzone, assignment):
    """
    Generate solution steps (states) that form a valid solution (see
    :func:`mmvdApp.utils.linprog.valid_solution`).

    :param array map_: warehouse map
    :param list robot_positions: starting positions of the robots
    :param list product_positions: positions where products are located
    :param list order: sequence of products to be delivered
    :param tuple dropzone: coords of drop-zone
    :param list assignment: robots → products assignment
    :return: states for specific solution
    :rtype: list
    """
    last_iteration_number = []
    routes = []

    # for each robot at each starting position generate route to the assigned
    # product
    for product_index, robot_index in enumerate(assignment):
        # product_positions - the same order as in `order`
        pos_y, pos_x = robot_positions[robot_index]

        distance1, _, route1 = a_star(map_, robot_positions[robot_index],
                                      product_positions[product_index])
        distance2, _, route2 = a_star(map_, product_positions[product_index],
                                      dropzone)

        # How many steps should wait at starting position.
        # Only 1 robot can start at one time, others have to wait to avoid
        # collisions.
        # Number of time to wait is calculated by measuring how many steps will
        # it take current robot to grab a product and go to dropzone.  Then
        # this number should be precisely 1 higher than drop-off step for the
        # robot with previous product, unless even without wait time it takes
        # current robot longer to reach drop-off step.
        delay_time = 0
        delay = []

        cumulated_time = 0
        for r_id, t in last_iteration_number:
            if r_id == robot_index:
                cumulated_time = t + 1

        if product_index > 0:
            _, delay_time = last_iteration_number[product_index - 1]
            delay_time += 1
            delay_time -= cumulated_time + distance1 + distance2
            if delay_time < 0:
                delay_time = 0

            # Anti-collision wait
            # Check existing states to see if we should wait one iteration more
            positions = [z[delay_time][1:3] for z in routes
                         if len(z) > delay_time]
            while (pos_y, pos_x) in positions:
                delay_time += 1
                positions = [z[delay_time][1:3] for z in routes
                             if len(z) > delay_time]

            delay = [(robot_index, pos_y, pos_x, None), ] * delay_time

        # This list holds a value that says:
        # > robot with `robot_index` will drop the i-th product at the
        # > `cum_time + delay + d1 + d2`-th state
        #
        # This list is used to calculate correct order of robots, for example:
        #   robot 2 has to wait for robot 1 to bring product A before robot 2
        #   can bring product B.  Robot 1 route's 6 long, but robot 2 route's
        #   only 4 long.  The requested products order is: A, B.  Therefore
        #   robot 2 has to wait for ca. 3 more steps before it dumps off
        #   product B.
        last_iteration_number.append(
            (robot_index, cumulated_time + delay_time + distance1 + distance2)
        )

        # Convert routes to states
        states1 = [(robot_index, pos_y, pos_x, None)]  # initial position
        states2 = [(robot_index, product_positions[product_index][0],
                    product_positions[product_index][1], order[product_index])]
        for pos_y, pos_x in route1:
            # Last item in state tuple is reserved for "carried" product.
            # Robot doesn't have the product until it reaches product's
            # position
            if product_positions[product_index] != (pos_y, pos_x):
                states1.append((robot_index, pos_y, pos_x, None))

        for pos_y, pos_x in route2:
            states2.append((robot_index, pos_y, pos_x, order[product_index]))

        # cumulate states
        all_states = delay + states1 + states2

        # join routes from the same robots
        # Quite common situation is when there are more products in order than
        # robots in warehouse.  Generated solution does not group routes by
        # robot.
        robot_appeared = -1
        robot_previous_length = 0
        for k, v in enumerate(routes):
            if v[0][0] == robot_index:
                robot_appeared = k
                all_states = routes[k] + all_states
                robot_previous_length += len(routes[k]) - 1
                # there should be only one cumulated route for each robot, so
                # it's save to assume we can break
                break

        # Find wait time.
        # If collisions occur, the robot should wait on its previous position
        i = robot_previous_length
        while i < len(all_states):
            r_id, pos_y, pos_x, _ = all_states[i]

            # find coords of other robots at the same state
            coords = [
                (v[i][1], v[i][2])
                for k, v in enumerate(routes)
                if len(routes[k]) > i and v[i][0] != r_id
            ]

            # check if any previous robot has the same coords at this state
            if (pos_y, pos_x) != dropzone and (pos_y, pos_x) in coords:
                # wait to avoid collision
                all_states.insert(i - 1, all_states[i - 1])

            i += 1

        # Finally add robot routes.
        # If there are no robots with this ID, simply add to the back;
        # otherwise re-assign robot routes, because `all_states` has cumulated
        # robot routes (ie. routes to+from different products)
        if robot_appeared == -1:
            routes.append(all_states)
        else:
            routes[robot_appeared] = all_states

    # to each robot's routes add drop-zone wait
    longest = max(map(len, routes))
    for k, v in enumerate(routes):
        difference = longest - len(v)  # difference is always >= 0
        if difference:
            x = v[-1]
            routes[k].extend([(x[0], x[1], x[2], None)] * difference)

    # convert routes for individual robots into one list of states that valid
    # solution consists of
    return zip(*routes)


def neighborhoods(solution):
    """
    Generate neighborhoods for given solution.

    :param list solution: arrangement (robots → products)
    :return: possible permutations of current solution
    :rtype: list
    """
    # TODO: come up with some neighborhoods

    # randomly select a robot index and generate swap with index-1 and index+1
    V = len(solution)
    i = random.randrange(V)
    i_1 = (i - 1) % V
    i_2 = (i + 1) % V
    sol1 = solution[:]
    sol2 = solution[:]
    sol1[i], sol1[i_1] = sol1[i_1], sol1[i]
    sol2[i], sol2[i_2] = sol2[i_2], sol2[i]

    # randomly change one robot with another
    i = random.randrange(V)
    sol3 = solution[:]
    Y = max(solution)
    sol3[i] = random.randrange(Y + 1)
    if sol3[i] == solution[i]:
        sol3[i] = (solution[i] + 1) % Y
    return [solution, sol1, sol2, sol3]
    # return [solution, sol1, sol2]


def best_candidate(map_, robot_positions, product_positions, candidates, order,
                   dropzone):
    """
    Select the best (robots → products) arrangement from all candidates.
    :func:`mmvdApp.utils.linprog.objective_function` provides a way to measure
    "fitness" of given arrangement.

    :param array map_: warehouse map
    :param list robot_positions: starting positions of the robots
    :param list product_positions: positions where products are located
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
        solution = generate_solution(map_, robot_positions, product_positions,
                                     order, dropzone, candidate)
        try:
            if valid_solution(solution, order, dropzone):
                objective = objective_function(solution)
                heapq.heappush(rv, (objective, candidate, solution))
        except (RobotCollisionException, InvalidOrderException):
            pass
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


def tabu_search(map_, robot_positions, product_positions, order,
                product_distances, rounds=10**3, memsize=5):
    """
    Compute best (not necessarily optimal) arrangement (robots → products),
    that is both valid (see :func:`mmvdApp.utils.linprog.valid_solution`) and
    has lowest available cost (see
    :func:`mmvdApp.utils.linprog.objective_function`).

    Computation is done using
    `Tabu search algorithm <http://en.wikipedia.org/wiki/Tabu_search>`_.

    :param array map_: a warehouse map
    :param list robot_positions: starting positions of the robots
    :param list product_positions: positions where products are located
    :param list order: a specific sequence of products that have to be dropped
                       in the dropzone in this specific order
    :param list product_distances: a helper list of distance tuples
                                   ``(to, from)`` the product on the map.
                                   Starting point is always dropzone, so is
                                   ending point.
    :param int rounds: number of loop iterations
    :param int memsize: number of taboo items to be held in short-term memory
    :return: a pair, ``result`` and ``solution``.  ``result`` carries best
             objective function value.  ``solution`` provides valid solution
             steps (as stated by :func:`mmvdApp.utils.linprog.valid_solution`
             function).
    """
    MAX_ITERATIONS = rounds
    MAX_TABU_SIZE = memsize
    dropzone = drop_zone(map_)

    solution = initial_solution(range(len(robot_positions)), order)
    best_solution = solution[:]  # copy of solution

    result = objective_function(solution)
    best_result = result

    best_solution_steps = generate_solution(map_, robot_positions,
                                            product_positions, order, dropzone,
                                            best_solution)

    tabu_list = collections.deque(maxlen=MAX_TABU_SIZE)

    i = 0
    while i < MAX_ITERATIONS:
        i += 1

        candidates = []
        for candidate in neighborhoods(best_solution):
            if features(best_solution, candidate) not in tabu_list:
                candidates.append(candidate)

        # best_candidate returns (result, candidate, solution_steps) tuple, but
        # we're not interested in the last one
        result, solution, steps = best_candidate(map_, robot_positions,
                                                 product_positions, candidates,
                                                 order, dropzone)
        if result < best_result:
            previous_solution = best_solution[:]
            best_solution = solution[:]
            best_result = result
            best_solution_steps = steps[:]

            tabu_list.append(features(previous_solution, solution))

    return best_result, best_solution, best_solution_steps
