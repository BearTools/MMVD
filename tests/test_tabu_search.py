# coding: utf-8
import pytest
from mmvdApp.utils.tabu import initial_solution, features, neighborhoods
from mmvdApp.utils.tabu import generate_solution
from mmvdApp.utils.linprog import (valid_solution, RobotCollisionException,
                                   InvalidOrderException)


@pytest.mark.utils
@pytest.mark.tabu
def test_initial_solution(warehouse_map1, robots_positions1, order1,
                          product_positions1, drop_zone1):
    robots = range(len(robots_positions1))
    solution = initial_solution(robots, order1)
    assert solution == [0, 1, 2, 0, 1, 2]
    steps = generate_solution(warehouse_map1, robots_positions1,
                              product_positions1, order1, drop_zone1, solution)
    assert valid_solution(steps, order1, drop_zone1)


@pytest.mark.utils
@pytest.mark.tabu
@pytest.mark.parametrize("previous,current,tabu", [
    ([0, 1, 2, 3], [0, 1, 3, 2], [None, None, 3, 2]),
    ([0, 1, 2, 3], [0, 1, 1, 3], [None, None, 1, None]),
    ([0, 0, 0, 0], [0, 1, 1, 3], [None, 1, 1, 3]),
])
def test_tabu_features(previous, current, tabu):
    assert features(previous, current) == tabu


@pytest.mark.utils
@pytest.mark.tabu
def test_tabu_neighborhoods():
    M = [0, 1, 2, 3, 4, 5]
    N = neighborhoods(M)
    assert len(N) == 4
    assert M in N

    # lists aren't hashable, that's why change to tuples
    assert len(set(tuple(x) for x in N)) == len(N)

    # 3rd neighborhood has exactly one robot repeated, one removed
    assert len(set(N[3])) == len(N[3]) - 1


@pytest.mark.utils
@pytest.mark.tabu
@pytest.mark.regression
@pytest.mark.parametrize("solution", [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 1, 2],
    [1, 1, 1, 1, 2, 0],
    [2, 2, 2, 2, 0, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 1, 0, 2, 1, 2],
    [1, 0, 2, 0, 1, 2],
])
def test_tabu_yield_valid_solution(warehouse_map1, robots_positions1, order1,
                                   product_positions1, drop_zone1, solution):
    steps = generate_solution(warehouse_map1, robots_positions1,
                              product_positions1, order1, drop_zone1, solution)
    import pprint
    pprint.pprint(steps)
    print len(steps)
    assert valid_solution(steps, order1, drop_zone1)
    assert 0


@pytest.mark.utils
@pytest.mark.tabu
@pytest.mark.regression
@pytest.mark.random
@pytest.mark.benchmark(
    group="random-solution-validness",
    min_rounds=10000,
    warmup=False,
)
@pytest.mark.slow
def test_tabu_yield_valid_solution_random(
        warehouse_map1, robots_positions1, order1, product_positions1,
        drop_zone1, initial_solution1, benchmark):

    @benchmark
    def loop():
        for neighbor in neighborhoods(initial_solution1):
            if neighbor != initial_solution1:
                # print "************"
                # print neighbor
                steps = generate_solution(warehouse_map1, robots_positions1,
                                          product_positions1, order1,
                                          drop_zone1, neighbor)
                # import pprint
                # pprint.pprint(steps)
                # print len(steps)
                assert valid_solution(steps, order1, drop_zone1)
