import pytest

from mmvdApp.shortest_path import neighbors
from mmvdApp.shortest_path import a_star as shortest_path


@pytest.mark.utils
@pytest.mark.parametrize("position,expected", [
    ((0, 0), ((1, 0),)),
    ((1, 1), ((1, 0), (2, 1), (0, 1))),
    ((4, 4), ((3, 4),)),
    ((2, 0), ((3, 0),)),
])
def test_neighbors(warehouse_map1, position, expected):
    assert expected == neighbors(warehouse_map1, position, available_only=True,
                                 positions=True)


@pytest.mark.utils
def test_neighbors2(warehouse_map1):
    position = (0, 0)
    assert (0, 2, 1, 0) == neighbors(warehouse_map1, position,
                                     available_only=False, positions=False)
    assert (None, (1, 0), (0, 1), None) == neighbors(warehouse_map1, position,
                                                     available_only=False,
                                                     positions=True)
    position = (1, 1)
    assert (2, 1, 'c', 1) == neighbors(warehouse_map1, position,
                                       available_only=False, positions=False)

    # this test is ridiculous (doesn't make any sense), but I do it anyway
    assert (2, 1, 1) == neighbors(warehouse_map1, position,
                                  available_only=True, positions=False)


@pytest.mark.utils
@pytest.mark.parametrize("start,end,path", [
    ((4, 4), (0, 0), [(4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 3), (0, 2),
                      (0, 1), (0, 0)]),
    ((0, 0), (2, 1), [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2),
                      (4, 3), (4, 4), (3, 4), (2, 4), (2, 3), (2, 2), (2, 1)]),
    ((4, 4), (3, 1), [(4, 4), (3, 4), (2, 4), (2, 3), (2, 2), (2, 1), (3, 1)])
])
def test_a_star(warehouse_map1, start, end, path):
    """
    Test accuracy and correctness of the A* algorithm.
    """
    length, iterations, final_path = shortest_path(warehouse_map1, start, end)
    assert length == len(path) - 1
    assert final_path == path
