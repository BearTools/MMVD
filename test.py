import pytest

from utils import read_warehouse_map
from utils import neighbors
from utils import a_star as shortest_path

from logic import Direction
from logic import Robot
from logic import Magazine


@pytest.fixture
def warehouse_map1(tmpdir):
    content = """22223
1a1b3
1c1d3
1e1f3
14449
"""
    file_ = tmpdir.join("warehouse.map")
    file_.write(content)
    return read_warehouse_map(str(file_), use_numpy=False)


@pytest.mark.frontend
def test_direction_class():
    direction = Direction()
    assert direction.get_up() is False
    direction.set_up(True)
    assert direction.get_up() is True
    direction.set_down(True)
    assert direction.get_down() is True
    assert direction.get_direction_list() == [True, False, True, False]


@pytest.mark.frontend
def test_robot_class():
    robot = Robot()
    direction_list = robot.get_direction().get_direction_list()
    assert direction_list == [False, False, False, False]
    robot.set_y(4)
    assert robot.get_y() == 4
    robot.set_direction(Direction(up=True, left=True))
    assert robot.get_direction().get_direction_list() == [True, False, False,
                                                          True]


@pytest.mark.frontend
def test_magazine_class():
    magazine = Magazine(5, 6)
    magazine.show()
    robot_array = ([[0, 1, 2, None],
                   [3, 2, 1, None]])
    arr = (
        [
            [2, 2, 2, 2, 3],
            [1, "a", 1, "B", 3],
            [1, "c", 1, "d", 3],
            [1, "e", 1, "f", 3],
            [1, "g", "h", "i", 3],
            [1, 4, 4, 4, 9],
        ]
    )
    magazine.update(arr, robot_array)
    arr = (
        [
            [2, 2, 2, 2, 3],
            [1, "a", 1, "b", 3],
            [1, "c", 1, "d", 3],
            [1, "e", 1, "f", 3],
            [1, "g", 4, "i", 3],
            [1, 4, 4, 9, 1],
        ]
    )
    magazine.update(arr, robot_array)
    arr = (
        [
            [2, 2, 2, 2, 3],
            [1, "a", 1, "H", 3],
            [1, "c", 1, "d", 3],
            [1, "e", 1, "f", 3],
            [1, 4, 4, 3, 3],
            [1, 1, 9, 1, 1],
        ]
    )
    magazine.update(arr, robot_array)
    magazine.end()


@pytest.mark.utils
def test_reading_warehouse_map(warehouse_map1):
    """
    Test if ``utils.read_warehouse_map`` works properly.
    """
    map_ = [
        [2,  2,  2,  2,  3],
        [1, "a", 1, "b", 3],
        [1, "c", 1, "d", 3],
        [1, "e", 1, "f", 3],
        [1,  4,  4,  4,  9],
    ]
    assert map_ == warehouse_map1


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
