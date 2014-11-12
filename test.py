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
    magazine = Magazine(width, height, [])
    magazine.get_tile(0, 0).set_dir(Direction(up=True))
    magazine.get_tile(width-1, 0).set_dir(Direction(left=True))
    magazine.get_tile(0, height-1).set_dir(Direction(right=True))
    magazine.get_tile(width-1, height-1).set_dir(Direction(down=True))
    for i in range(1, width-1):
        magazine.get_tile(i, 0).set_dir(Direction(True, False, False, True))
        magazine.get_tile(i, height-1).set_dir(Direction(right=True))

    for i in range(1, height-1):
        magazine.get_tile(0, i).set_dir(Direction(up=True, right=True))
        magazine.get_tile(width-1, i).set_dir(Direction(down=True,
                                                       left=True))
        for j in range(1, width-1, 3):
            magazine.get_tile(j, i).set_dir(Direction(left=True))
        for j in range(2, width-1, 3):
            magazine.get_tile(j, i).set_dir(Direction(right=True))
        for j in range(3, width-1, 3):
            magazine.get_tile(j, i).set_dir(Direction(up=True, left=True,
                                                      right=True))
    return magazine


def visualize_test():
    pos = Position(1, 1)
    robot = Robot(pos, Direction())
    robot_list = []
    robot_list.append(robot)
    magazine = build_magazine(15, 15)  # build 15x15 magazine with simple rules
    magazine.add_robot(robot)
    animation = RobotVisualization(len(magazine.get_robots()),
                                   magazine.get_width(),
                                   magazine.get_height())
    for i in range(200):

        for robot in magazine.get_robots():
            robot.set_dir(magazine.get_tile(
                robot.get_pos().get_x(), robot.get_pos().get_y()).get_dir())
            if robot.get_dir().get_up():
                robot.set_pos(Position(robot.get_pos().get_x(), robot.get_pos().get_y() + 1))
            elif robot.get_dir().get_right():
                robot.set_pos(Position(robot.get_pos().get_x() + 1, robot.get_pos().get_y()))
            elif robot.get_dir().get_down():
                robot.set_pos(Position(robot.get_pos().get_x(), robot.get_pos().get_y() - 1))
            elif robot.get_dir().get_left():
                robot.set_pos(Position(robot.get_pos().get_x() - 1, robot.get_pos().get_y()))
            print robot.get_dir()
            print robot.get_pos()
        animation.update(magazine, magazine.get_robots())
    animation.done()


visualize_test()
#buildMagazin(15,15)

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



print read_warehouse_map('test_data/magazine1.map')