# coding: utf-8
import pytest
from mmvdApp.utils.tabu import initial_solution


@pytest.mark.utils
@pytest.mark.tabu
def test_initial_solution(robots_positions1, order1):
    robots = range(len(robots_positions1))
    assert initial_solution(robots, order1) == [0, 1, 2, 0, 1, 2]
