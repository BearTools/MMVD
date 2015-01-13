# coding: utf-8
import pytest
from mmvdApp.utils import objective_function
from mmvdApp.utils import valid_solution
from mmvdApp.utils import InvalidOrderException


@pytest.mark.utils
@pytest.mark.linprog
def test_objective_function(states1):
    """
    Test if ``utils.linprog.objective_function`` correctly calculates expected
    objective function value.
    """
    assert objective_function(states1) == 17


@pytest.mark.utils
@pytest.mark.linprog
def test_solution_validity(states1, order1, drop_zone1):
    """
    Test if ``utils.linprog.valid_solution`` correctly checks for valid
    solution.
    """
    # cut order in half because states1 is intended only for first 3 products
    order = order1[0:3]

    assert valid_solution(states1, order, drop_zone1)

    # check for valid solution when one product isn't returned
    with pytest.raises(InvalidOrderException):
        valid_solution(states1[0:-1], order, drop_zone1)
