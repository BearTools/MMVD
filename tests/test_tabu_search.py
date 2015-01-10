# coding: utf-8
import pytest
from mmvdApp.utils.tabu import initial_solution, features


@pytest.mark.utils
@pytest.mark.tabu
def test_initial_solution(robots_positions1, order1):
    robots = range(len(robots_positions1))
    assert initial_solution(robots, order1) == [0, 1, 2, 0, 1, 2]


@pytest.mark.utils
@pytest.mark.tabu
@pytest.mark.parametrize("previous,current,tabu", [
    ([0, 1, 2, 3], [0, 1, 3, 2], [None, None, 3, 2]),
    ([0, 1, 2, 3], [0, 1, 1, 3], [None, None, 1, None]),
    ([0, 0, 0, 0], [0, 1, 1, 3], [None, 1, 1, 3]),
])
def test_tabu_features(previous, current, tabu):
    assert features(previous, current) == tabu
