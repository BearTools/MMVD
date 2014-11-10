__author__ = 'wojciech'


#

class Position(object):
    '''
    Position represents a location in magazine
    '''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def updatePosition(self):
        '''

        :return: returns new position after a clock tic
        '''
        raise NotImplementedError


class Direction(object):
    '''
    Directions encoding is as follow:
    4 fields (up right, down, left) each true or false depending if it is possible to
    go in indicated direction
    '''

    def __init__(self, up = False, right = False, down = False, left = False ):

        # initialises direction, Assumes that if direction is not specified,than
        # it is marked as disabled

        self.up = up
        self.right = right
        self.down = down
        self.left = left

    def getUp(self):
        return self.up

    def getRight(self):
        return self.right

    def getDown(self):
        return self.down

    def getLeft(self):
        return self.left

    def getDirections(self):

        # return: list of possible directions for a tile

        list = []
        list.append(self.up)
        list.append(self.right)
        list.append(self.down)
        list.append(self.left)
        return list

    def setDirections(self, up=False, right=False, down=False, left=False ):
        self.up = up
        self.right = right
        self.down = down
        self.left = left

    def __str__(self):

        text = '{:6s}{:2s}{:5s}'.format('Up',' : ', str(self.getUp()))
        text += '\n'
        text += '{:6s}{:2s}{:5s}'.format('Right',' : ', str(self.getRight()))
        text += '\n'
        text += '{:6s}{:2s}{:5s}'.format('Down',' : ', str(self.getDown()))
        text += '\n'
        text += '{:6s}{:2s}{:5s}'.format('Left',' : ', str(self.getLeft()))
        return text

class Magazine(object):
    '''
    Represents magazine as 2 dimensional array. each tile is marked with
    direction in which robot can move from the tile.

    It is possible for the tiles to change possible directions with time when there
    shows up shortcut. // Not yet implemented

    directions encoding is as follow:
    4 fields (up right, down, left) each true or false depending if it is possible to
    go in indicated direction

    robot_list is list of all robots in the magazine

    shelf_list is list of all shelf in the magazine

    '''

    def __init__(self, width, height, robot_list):
        self.width = width
        self.height = height
        self.area = [[Direction() for i in range(height)]for j in range(width)]
        self.robot_list = robot_list

    def getTileDirections(self, pos):
        '''
        :param pos: position of a tile
        :return: dir for tile at position pos
        '''
        return self.area[pos.getX][pos.getY].getDirections()


    def setTileDirection(self, pos, dir):
        '''
        sets dir to a tile at pos
        :param pos:
        :param dir:
        :return:
        '''
        self.area[pos.getX][pos.getY].setDirections(dir)

    def __str__(self):
        text = ''
        for i in range(self.width):
            for j in range(self.height):
                text += str(self.area[i][j].getDirections())
            text += '\n'
        return text

    def getRobots(self):
        return self.robot_list

    def addRobot(self, robot):
        self.robot_list.append(robot)

    def setRobots(self,robot_list):
        self.robot_list = robot_list


class Robot(object):
    '''
    Represents robot.
    Defines position of robot.
    Defines all possible direction for a robot to go in the next step
    Keeps track of shelf being carried by robot
    Has his
    '''
    def __init__(self, pos=Position(0,0), _dir=Direction()):
        self.pos = pos
        self.dir = _dir
        #self.shelf = shelf shelf not implemented


    def setPos(self, pos):
        self.pos = pos

    def getPos(self):
        return self.pos

    def setDir(self, dir):
        self.dir = dir

    def getDir(self):
        return self.dir


class Shelf(object):
    '''
    Represents shelf. Keeps track of what is in the shelf as well as keeps current
    position.
    knows its default/initial position in magazine
    '''
    def __init__(self):
        raise NotImplementedError
