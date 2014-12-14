import pytest

from mmvdApp.logic import Direction
from mmvdApp.logic import Robot
from mmvdApp.logic import Magazine


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
    # TODO: for some strange reason, .end() only keeps application running
    # magazine.end()
