__author__ = 'wojciech'

from Logic import *
from visualize import *
from utils import *


def build_magazine(width, height):
    """
    input width, height of magazine
    output magazine object
    Builds magazine with very simple topology.
    There are roads that lead up for every shelf
    exit points and shelfs will be implemented in the future
    """
    magazine = Magazine(width, height)
    magazine.get_tile(0, 0).set_direction(Direction(up=True))
    magazine.get_tile(width-1, 0).set_direction(Direction(left=True))
    magazine.get_tile(0, height-1).set_direction(Direction(right=True))
    magazine.get_tile(width-1, height-1).set_direction(Direction(down=True))
    for i in range(1, width-1):
        magazine.get_tile(i, 0).set_direction(Direction(True, False, False, True))
        magazine.get_tile(i, height-1).set_direction(Direction(right=True))

    for i in range(1, height-1):
        magazine.get_tile(0, i).set_direction(Direction(up=True, right=True))
        magazine.get_tile(width-1, i).set_direction(Direction(down=True,
                                                       left=True))
        for j in range(1, width-1, 3):
            magazine.get_tile(j, i).set_direction(Direction(left=True))
        for j in range(2, width-1, 3):
            magazine.get_tile(j, i).set_direction(Direction(right=True))
        for j in range(3, width-1, 3):
            magazine.get_tile(j, i).set_direction(Direction(up=True, left=True,
                                                      right=True))
    return magazine


def visualize_test():
    x = 1
    y = 1
    robot = Robot(x, y, Direction())
    robot_list = []
    robot_list.append(robot)
    magazine = build_magazine(15, 15)  # build 15x15 magazine with simple rules
    magazine.add_robot(robot)
    animation = RobotVisualization(len(magazine.get_robot_list()),
                                   magazine.get_width(),
                                   magazine.get_height())
    for i in range(20):

        for robot in magazine.get_robot_list():
            robot.set_direction(magazine.get_tile(
                robot.get_x(), robot.get_y()).get_direction())
            if robot.get_direction().get_up():
                robot.set_x(robot.get_x())
                robot.set_y(robot.get_y() + 1)
                magazine.get_tile(1,1).set_direction(Direction(True,True,True,True))
            elif robot.get_direction().get_right():
                robot.set_x(robot.get_x() + 1)
                robot.set_y(robot.get_y())
                magazine.get_tile(1,1).set_direction(Direction(True,False,True,True))
            elif robot.get_direction().get_down():
                robot.set_x(robot.get_x())
                robot.set_y(robot.get_y() - 1)
                magazine.get_tile(1,1).set_direction(Direction(True,False,True,True))
            elif robot.get_direction().get_left():
                robot.set_x(robot.get_x() - 1)
                robot.set_y(robot.get_y())
                magazine.get_tile(1,1).set_direction(Direction(True,False,True,True))
            print robot.get_direction()
            print str(robot.get_x()) + " " + str(robot.get_y())

        animation.update(magazine, magazine.get_robot_list())
    animation.done()


def test_reading_warehouse_map(tmpdir):
    """
    Test if ``utils.read_warehouse_map`` works properly.
    """
    from utils import read_warehouse_map
    content = """22223
1a1b3
1c1d3
1e1f3
14449
"""
    file_ = tmpdir.join("warehouse.map")
    file_.write(content)
    map_ = [
        [2, 2, 2, 2, 3],
        [1, "a", 1, "b", 3],
        [1, "c", 1, "d", 3],
        [1, "e", 1, "f", 3],
        [1, 4, 4, 4, 9],
    ]

    print map_
    array = read_warehouse_map(str(file_), use_numpy=False)
    assert map_ == array


def test_direction_class():
    direction = Direction()
    assert direction.get_up() == False
    direction.set_up(True)
    assert direction.get_up() == True
    direction.set_down(True)
    assert direction.get_down() == True
    assert direction.get_direction_list() == [True, False, True, False]


def test_robot_class():
    robot = Robot()
    assert robot.get_direction().get_direction_list() == [False, False, False, False]
    robot.set_y(4)
    assert robot.get_y() == 4
    robot.set_direction(Direction(up=True, left=True))
    assert robot.get_direction().get_direction_list() == [True, False, False, True]


def test_magazine_class():
    magazine = Magazine(5, 6)
    magazine.show()
    robot_array = ([[0, 1, 2, None],
                   [3, 2, 1, None]])
    arr = ([[2, 2, 2, 2, 3],
           [1, "a", 1, "B", 3],
           [1, "c", 1, "d", 3],
           [1, "e", 1, "f", 3],
           [1, "g", "h","i", 3],
           [1, 4, 4, 4, 9],
    ])
    magazine.update(arr, robot_array)
    arr = ([[2, 2, 2, 2, 3],
            [1, "a", 1, "b", 3],
            [1, "c", 1, "d", 3],
            [1, "e", 1, "f", 3],
            [1, "g", 4, "i", 3],
            [1, 4, 4, 9, 1],
    ])
    magazine.update(arr,robot_array)
    arr = ([[2, 2, 2, 2, 3],
            [1, "a", 1, "H", 3],
            [1, "c", 1, "d", 3],
            [1, "e", 1, "f", 3],
            [1, 4, 4, 3, 3],
            [1, 1, 9, 1, 1],
    ])
    magazine.update(arr, robot_array)
    magazine.end()




if __name__ == "__main__":
    test_magazine_class()
    test_direction_class()
    test_robot_class()
