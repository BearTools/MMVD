import pytest
from mmvdApp.utils import objective_function
from mmvdApp.utils import valid_solution


@pytest.mark.utils
@pytest.mark.LP
def test_objective_function(states1):
    """
    Test if ``utils.LP.objective_function`` correctly calculates expected
    objective function value.
    """
    assert objective_function(states1) == 17


@pytest.mark.utils
@pytest.mark.LP
def test_solution_validity(states1, order1, drop_zone1):
    """
    Test if ``utils.LP.valid_solution`` correctly checks for valid solution.
    """
    assert valid_solution(states1, order1, drop_zone1)
    # check for valid solution when one product isn't returned
    assert not valid_solution(states1[0:-1], order1, drop_zone1)
