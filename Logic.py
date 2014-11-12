__author__ = 'wojciech'


class Position(object):
    """
    Position represents a location in magazine
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def update_position(self):
        """
        It is used when robot tries to update its position.
        :return: returns new position after a clock tic
        """
        raise NotImplementedError

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


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

    def get_up(self):
        return self.up

    def set_up(self, up=True):
        self.up = up

    def get_right(self):
        return self.right

    def set_right(self, right=True):
        self.right = right

    def get_down(self):
        return self.down

    def set_down(self, down=True):
        self.down = down

    def get_left(self):
        return self.left

    def set_left(self, left=True):
        self.left = left

    def get_directions(self):
        """
        Return list of possible directions for a tile
        """
        list_ = []
        list_.append(self.up)
        list_.append(self.right)
        list_.append(self.down)
        list_.append(self.left)
        return list_

    def set_directions(self, up=False, right=False, down=False, left=False):
        self.up = up
        self.right = right
        self.down = down
        self.left = left

    def __str__(self):
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

    """

    def __init__(self, width, height, robot_list):
        self.width = width
        self.height = height
        self.tiles = [[Tile(Position(j, i), Direction()) for i in range(height)] for j in range(width)]
        self.robot_list = robot_list

    def get_tile_directions(self, pos):
        """
        :param pos: position of a tile
        :return: dir for tile at position pos
        """
        return self.tiles[pos.get_x()][pos.get_y()].get_dir()

    def set_tile_direction(self, pos, dir_):
        """
        sets dir to a tile at pos
        :param pos:
        :param dir_:
        :return:
        """
        self.tiles[pos.get_x][pos.get_y].set_dir(dir_)

    def get_tile(self, x, y):
        return self.tiles[x][y]

    def __str__(self):
        text = ''
        for i in range(self.width):
            for j in range(self.height):
                text += str(self.tiles[i][j].get_dir())
            text += '\n'
        return text

    def get_robots(self):
        return self.robot_list

    def add_robot(self, robot):
        self.robot_list.append(robot)

    def set_robots(self, robot_list):
        self.robot_list = robot_list

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class Robot(object):
    """
    Represents robot.
    Defines position of robot.
    Defines all possible direction for a robot to go in the next step
    Keeps track of shelf being carried by robot
    Has his
    """
    def __init__(self, pos=None, _dir=Direction()):
        if not pos:
            pos = Position(0, 0)
        self.pos = pos
        self.dir = _dir
        #self.shelf = shelf shelf not implemented

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def set_dir(self, dir_):
        self.dir = dir_

    def get_dir(self):
        return self.dir

    def __str__(self):
        return str(self.pos) + '\n' + str(self.dir)


class Tile(object):
    """
    Single tile in the magazine. Has position, and possible direction.
    """
    def __init__(self, pos, dir_):
        self.pos = pos
        self.dir = dir_

    def get_pos(self):
        return self.pos

    def get_dir(self):
        return self.dir

    def set_pos(self, pos):
        self.pos = pos

    def set_dir(self, dir_):
        self.dir = dir_


class Shelf(object):
    """
    Represents shelf. Keeps track of what is in the shelf as well as keeps
    current position.
    Knows its default/initial position in magazine.
    item_list - list of all products that are in the shelf
    """
    def __init__(self):
        raise NotImplementedError