__author__ = 'wojciech'

from Logic import *
from visualize import *


def build_magazine(width, height):
    """
    Build simple magazin.  There are no exit points, nor shelfs.  These will be
    implemented in the future.
    """
    magazine = Magazine(width, height, [])
    magazine.getTile(0, 0).setDir(Direction(up=True))
    magazine.getTile(width-1, 0).setDir(Direction(left=True))
    magazine.getTile(0, height-1).setDir(Direction(right=True))
    magazine.getTile(width-1, height-1).setDir(Direction(down=True))
    for i in range(1, width-1):
        magazine.getTile(i, 0).setDir(Direction(True, False, False, True))
        magazine.getTile(i, height-1).setDir(Direction(right=True))

    for i in range(1, height-1):
        magazine.getTile(0, i).setDir(Direction(up=True, right=True))
        magazine.getTile(width-1, i).setDir(Direction(down=True, left=True))
        for j in range(1, width-1, 3):
            magazine.getTile(j, i).setDir(Direction(left=True))
        for j in range(2, width-1, 3):
            magazine.getTile(j, i).setDir(Direction(right=True))
        for j in range(3, width-1, 3):
            magazine.getTile(j, i).setDir(Direction(up=True, left=True,
                                                    right=True))
    return magazine


def visualize_test():
    pos = Position(1, 1)
    robot = Robot(pos, Direction())
    robot_list = []
    robot_list.append(robot)
    magazine = build_magazine(15, 15)
    magazine.addRobot(robot)
    animation = RobotVisualization(len(magazine.getRobots()),
                                   magazine.getWidth(),
                                   magazine.getHeight())
    for i in range(200):

        for robot in magazine.getRobots():
            robot.setDir(magazine.getTile(
                robot.getPos().getX(), robot.getPos().getY()).getDir())
            if robot.getDir().getUp():
                robot.setPos(Position(robot.getPos().getX(), robot.getPos().getY() + 1))
            elif robot.getDir().getRight():
                robot.setPos(Position(robot.getPos().getX() + 1, robot.getPos().getY()))
            elif robot.getDir().getDown():
                robot.setPos(Position(robot.getPos().getX(), robot.getPos().getY() - 1))
            elif robot.getDir().getLeft():
                robot.setPos(Position(robot.getPos().getX() - 1, robot.getPos().getY()))
            print robot.getDir()
            print robot.getPos()
        animation.update(magazine, magazine.getRobots())
    animation.done()


# visualize_test()
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
    array = read_warehouse_map(str(file_), use_numpy=False)
    assert map_ == array
