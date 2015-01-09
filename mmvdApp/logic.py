__author__ = 'wojciech'

from visualize import *


class Direction(object):
    """
    Directions encoding is as follow:
    4 fields (up right, down, left) each True or False depending on it's
    ability to follow indicated direction.
    """

    def __init__(self, up=False, right=False, down=False, left=False):

        # initialises direction, Assumes that if direction is not specified,
        # then it is marked as disabled

        self.up = up
        self.right = right
        self.down = down
        self.left = left

    def get_down(self):
        return self.down

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_up(self):
        return self.up

    def set_down(self, down=True):
        self.down = down

    def set_left(self, left=True):
        self.left = left

    def set_right(self, right=True):
        self.right = right

    def set_up(self, up=True):
        self.up = up

    def get_direction_list(self):
        """
        Return list of possible directions for a tile
        """
        list_ = [self.up, self.right, self.down, self.left]
        return list_

    def set_direction(self, up=False, right=False, down=False, left=False):
        self.up = up
        self.right = right
        self.down = down
        self.left = left

    def __str__(self):
        """
        __str__ function has to be modified in a way so it is easy to save
        it in a file as proposed in utils.py
        """
        text = '{:6s}{:2s}{:5s}'.format('Up', ' : ', str(self.get_up()))
        text += '\n'
        text += '{:6s}{:2s}{:5s}'.format('Right', ' : ', str(self.get_right()))
        text += '\n'
        text += '{:6s}{:2s}{:5s}'.format('Down', ' : ', str(self.get_down()))
        text += '\n'
        text += '{:6s}{:2s}{:5s}'.format('Left', ' : ', str(self.get_left()))
        return text


class Magazine(object):
    """
    Represents magazine as 2 dimensional array. each tile is marked with
    direction in which robot can move from the tile.

    It is possible for the tiles to change possible directions with time when
    there shows up shortcut. (Not yet implemented)

    Directions encoding is as follow:
    4 fields (up right, down, left) each true or false depending on it's
    ability to follow indicated direction.

    robot_list is list of all robots in the magazine

    shelf_list is list of all shelf in the magazine

    1. Specify dimensions of magazine
        magazine = Magazine(width, height)
        # width = number of columns in array
        a) each dimension must be bigger or equal to 1
    2. Start loop {
        1. Create/load array representing magazine at each moment
            a) dimensions of array must agree with dimensions of magazine
               # width = number of columns in array
               # height = number of rows in array
        2. magazine.update(array)
            # forces new magazine to be displayed
        }
    3 magazine.end()
        #closes animation. Releases window handler.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [
            [Tile(j, i, Direction()) for i in range(height)]
            for j in range(width)
        ]
        self.robot_list = []
        self.shelf_list = []
        self.visualize = RobotVisualization
        self.exit_points = []

    def add_robot(self, robot):
        self.robot_list.append(robot)

    def add_shelf(self, shelf):
        self.shelf_list.append(shelf)

    def build_from_array(self, array, robot_array):
        """
        Very important function!
        Creates magazine based on content of array
        """
        self.exit_points = []
        self.shelf_list = []
        for i in range(len(array)):
            for j in range(len(array[i])):
                if array[i][j] == 1:
                    self.get_tile(j, len(array) - i - 1) \
                        .set_direction(Direction(up=True))
                elif array[i][j] == 2:
                    self.get_tile(j, len(array) - i - 1) \
                        .set_direction(Direction(right=True))
                elif array[i][j] == 3:
                    self.get_tile(j, len(array) - i - 1) \
                        .set_direction(Direction(down=True))
                elif array[i][j] == 4:
                    self.get_tile(j, len(array) - i - 1) \
                        .set_direction(Direction(left=True))
                elif array[i][j] == 9:
                    self.exit_points.append((j, len(array) - i - 1))
                    self.get_tile(j, len(array) - 1 - i) \
                        .set_direction(Direction())
                else:
                    self.shelf_list.append(Shelf(j, len(array) - 1 - i,
                                                 array[i][j]))
                    self.get_tile(j, len(array) - 1 - i) \
                        .set_direction(Direction())
                    continue

        for robot_index in range(len(robot_array)):
            if len(self.robot_list) < len(robot_array):
                for robot in robot_array:
                    self.robot_list.append(Robot())
            self.robot_list[robot_index].set_x(robot_array[robot_index][0])
            self.robot_list[robot_index] \
                .set_y(self.get_height() - 1 - robot_array[robot_index][1])
            if robot_array[robot_index][2] == 1:
                self.robot_list[robot_index].set_direction(Direction(up=True))
            elif robot_array[robot_index][2] == 2:
                self.robot_list[robot_index] \
                    .set_direction(Direction(right=True))
            elif robot_array[robot_index][2] == 3:
                self.robot_list[robot_index] \
                    .set_direction(Direction(down=True))
            elif robot_array[robot_index][2] == 4:
                self.robot_list[robot_index] \
                    .set_direction(Direction(left=True))

    def show(self):
        self.visualize = RobotVisualization(self.get_width(),
                                            self.get_height())

    def oldUpdate(self, map_, robot_array):
        self.build_from_array(map_, robot_array)
        self.visualize.oldUpdate(self, self.get_robot_list())

    def end(self):
        self.visualize.done()

    def get_exit_points(self):
        return self.exit_points

    def get_height(self):
        return self.height

    def get_robot_list(self):
        return self.robot_list

    def get_shelf_list(self):
        return self.shelf_list

    def get_tile(self, x, y):
        return self.tiles[x][y]

    def get_width(self):
        return self.width

    def set_robots(self, robot_list):
        self.robot_list = robot_list

    def set_tile_direction(self, x, y, dir_):
        self.tiles[x][y].set_direction(dir_)

    def __str__(self):
        text = ''
        for i in range(self.width):
            for j in range(self.height):
                text += str(self.tiles[i][j].get_direction())
            text += '\n'
        return text


class Robot(object):
    """
    Represents robot.
    Defines position of robot as coordinates (x, y)
    Defines all possible direction for a robot to go in the next step
    Keeps track of shelf being carried by robot
    """
    def __init__(self, x=0, y=0, _dir=Direction()):
        self.x = x
        self.y = y
        self.dir = _dir
        #self.shelf = Shelf()

    def get_direction(self):
        return self.dir

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_direction(self, dir_):
        self.dir = dir_

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')\n' + str(self.dir)


class Tile(object):
    """
    Single tile in the magazine. Has position, and possible direction.
    """
    def __init__(self, x, y, dir_=Direction()):
        self.x = x
        self.y = y
        self.dir = dir_

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_direction(self):
        return self.dir

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_direction(self, dir_):
        self.dir = dir_


class Shelf(object):
    """
    Represents shelf. Keeps track of what is in the shelf as well as keeps
    current position.
    Knows its position in magazine.
    Name has to be unique for each shelf
    Name is to be displayed when animation runs
    """
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_name(self, name):
        self.name = name

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
