# coding: utf-8

"""
LinProg stands for Linear Programming.  Functions defined here are intended for
specific operational research calculations.
"""


def valid_solution(solution, order, dropzone):
    """
    Check validity of a given solution sequence.

    Solution is valid if and only if products are dropped in drop-zone in order
    specified by parameter `order`.

    :rtype: boolean
    :return: check if solution is valid
    """
    dropped = []  # sequence of products dropped by robots in the drop-zone

    # TODO: can optimize by checking order on the fly
    for state in solution:
        # check if products are getting dropped
        for robot, pos_y, pos_x, product in state:
            if (pos_y, pos_x) == dropzone and product:
                dropped.append(product)

    # check if dropped products appear in the same order as they should
    return dropped == order


def objective_function(states):
    """
    Calculate objective function value for given states.

    A state in this application corresponds to positions and cargo of all
    robots in the warehouse.
    A sequence of such states represents robots movements.  This sequence can
    be a valid solution if at the end all required products were carried by
    robots to their drop zone.

    **WARNING**: this function does **not** check solution for validity.

    :param states: a sequence of application states
    :rtype: int
    :return: number specifying how much time did it take to complete the order
    """
    return len(states)
