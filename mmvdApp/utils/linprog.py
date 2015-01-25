# coding: utf-8
from .memoization import memoize

"""
LinProg stands for Linear Programming.  Functions defined here are intended for
specific operational research calculations.
"""


class RobotCollisionException(Exception):
    """
    This exception indicates that in the specific solution steps at least
    two robots have the same coordinates (!= drop zone) at the same time.
    """
    def __init__(self, arg):
        super(RobotCollisionException, self).__init__(arg)
        self.arg = arg


class InvalidOrderException(Exception):
    """
    Raised by :func:`mmvdApp.utils.linprog.valid_solution` when provided
    solution doesn't bring selected products in specified order.
    """
    def __init__(self, arg):
        super(InvalidOrderException, self).__init__(arg)
        self.arg = arg


@memoize
def valid_solution(solution, order, dropzone):
    """
    Check validity of a given solution sequence.

    Solution is valid if and only if products are dropped in drop-zone in order
    specified by parameter `order`.

    :rtype: bool
    :return: check if solution is valid
    """
    dropped = []  # sequence of products dropped by robots in the drop-zone

    for state_id, state in enumerate(solution):
        # check if products are getting dropped
        positions = []
        positions_set = set()

        for robot, pos_y, pos_x, product in state:
            if (pos_y, pos_x) == dropzone and product:
                dropped.append(product)
            if (pos_y, pos_x) != dropzone:
                positions.append((pos_y, pos_x))
                positions_set.add((pos_y, pos_x))

        if len(positions) != len(positions_set):
            number = len(positions) - len(positions_set)
            raise RobotCollisionException("{number} of robots collide on "
                                          "positions {positions} on state no. "
                                          "{id}"
                                          .format(number=number, id=state_id,
                                                  positions=positions))

    # check if dropped products appear in the same order as they should
    if tuple(dropped) != order:
        raise InvalidOrderException("Products should be provided in this "
                                    "order: {order}, but got {dropped} "
                                    "instead".format(order=order,
                                                     dropped=dropped))
    return True


def objective_function(states):
    """
    Calculate objective function value for given states.

    A state in this application corresponds to positions and cargo of all
    robots in the warehouse.
    A sequence of such states represents robots movements.  This sequence can
    be a valid solution if at the end all required products were carried by
    robots to their drop zone.

    .. warning::
        This function does **not** check solution for validity.  Use
        :func:`mmvdApp.utils.linprog.valid_solution` instead.

    :param states: a sequence of application states
    :rtype: int
    :return: number specifying how much time did it take to complete the order
    """
    return len(states)
