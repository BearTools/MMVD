__author__ = 'wojciech'

#import math
import time

from Tkinter import *


class RobotVisualization:
    """
    Visualization of magazine. Shows view of magazine from above.

    """
    def __init__(self,  width, height, delay=0.5):
        """
        Initializes a visualization with the specified parameters.

        """
        # Number of seconds to pause after each frame
        self.delay = delay
        self.windowSize = 600

        self.max_dim = max(width, height)
        self.width = width
        self.height = height

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=self.windowSize + 50,
                        height=self.windowSize + 50)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill="white")

        self.tiles = {}
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                self.tiles[(i, j)] = \
                    self.w.create_rectangle(x1, y1,
                                            x2, y2,
                                            fill="gray")

        # Draw grid lines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)

        # Draw some status text
        self.robots = None
        self.robotsDirections = None
        self.tilesDirections = None
        self.exit_points = None
        self.shelfs = None
        self.shelfs_names = None
        self.text = self.w.create_text(25, 0, anchor=NW,
                                       text=self._status_string(0))
        self.time = 0
        self.master.update()

    def _status_string(self, time_):
        """
        Prints current time at the top
        """
        return "Time: %04d; " % \
            time_

    def _map_coords(self, x, y):
        """
        Maps grid positions to window positions (in pixels).
        """
        return (self.windowSize/2 + 25 + self.windowSize *
                ((x - self.width / 2.0) / self.max_dim),
                self.windowSize/2 + 25 + self.windowSize *
                ((self.height / 2.0 - y) / self.max_dim))

# -----------------------------------------------------------------
    # set of functions to update all robots in the area with all directions
    # possible for each of robots.
    # This way of adding elements allows to delete them from visualisation
    # There definitely is a better way of doing this.
    def _draw_robot(self, robot):
        x, y = robot.get_x(), robot.get_y()
        tile_size = self.windowSize/self.max_dim
        x0, y0, = self._map_coords(x, y)
        return self.w.create_oval(x0 + int(tile_size*0.2),
                                  y0 - int(tile_size*0.2),
                                  x0 + int(tile_size*0.8),
                                  y0 - int(tile_size*0.8),
                                  fill="red")

    def _draw_robot_up(self, robot):
        x, y = robot.get_x(), robot.get_y()
        tile_size = self.windowSize/self.max_dim
        x0, y0, = self._map_coords(x, y)
        direction = robot.get_direction()
        if direction.get_up():
            x1 = x0 + int(tile_size*0.4)
            y1 = y0 - int(tile_size*0.65)
            x2 = x0 + int(tile_size*0.6)
            y2 = y0 - int(tile_size*0.65)
            x3 = x0 + int(tile_size*0.5)
            y3 = y0 - int(tile_size*0.73)
            return self.w.create_polygon(
                x1, y1, x2, y2, x3, y3, fill="darkgreen")

    def _draw_robot_right(self, robot):
        x, y = robot.get_x(), robot.get_y()
        tile_size = self.windowSize/self.max_dim
        x0, y0, = self._map_coords(x, y)
        direction = robot.get_direction()
        if direction.get_right():
            x1 = x0 + int(tile_size*0.73)
            y1 = y0 - int(tile_size*0.5)
            x2 = x0 + int(tile_size*0.65)
            y2 = y0 - int(tile_size*0.4)
            x3 = x0 + int(tile_size*0.65)
            y3 = y0 - int(tile_size*0.6)
            return self.w.create_polygon(
                x1, y1, x2, y2, x3, y3, fill="darkgreen")

    def _draw_robot_down(self, robot):
        x, y = robot.get_x(), robot.get_y()
        tile_size = self.windowSize/self.max_dim
        x0, y0, = self._map_coords(x, y)
        direction = robot.get_direction()
        if direction.get_down():
            x1 = x0 + int(tile_size*0.4)
            y1 = y0 - int(tile_size*0.35)
            x2 = x0 + int(tile_size*0.6)
            y2 = y0 - int(tile_size*0.35)
            x3 = x0 + int(tile_size*0.5)
            y3 = y0 - int(tile_size*0.27)
            return self.w.create_polygon(
                x1, y1, x2, y2, x3, y3, fill="darkgreen")

    def _draw_robot_left(self, robot):
        x, y = robot.get_x(), robot.get_y()
        tile_size = self.windowSize/self.max_dim
        x0, y0, = self._map_coords(x, y)
        direction = robot.get_direction()
        if direction.get_left():
            x1 = x0 + int(tile_size*0.27)
            y1 = y0 - int(tile_size*0.5)
            x2 = x0 + int(tile_size*0.35)
            y2 = y0 - int(tile_size*0.4)
            x3 = x0 + int(tile_size*0.35)
            y3 = y0 - int(tile_size*0.6)
            return self.w.create_polygon(
                x1, y1, x2, y2, x3, y3, fill="darkgreen")

# -------------------------------------------------------------------------
    # set of functions to update all possible directions for a given tile
    # This way of adding elements allows to delete them from visualisation
    # There definitely is a better way of doing this.

    def _draw_dir_up(self, x, y, up):
        tile_size = self.windowSize/self.max_dim
        x0, y0 = self._map_coords(x, y)
        if up:
            x1 = x0 + int(tile_size*0.4)
            y1 = y0 - int(tile_size*0.85)
            x2 = x0 + int(tile_size*0.6)
            y2 = y0 - int(tile_size*0.85)
            x3 = x0 + int(tile_size*0.5)
            y3 = y0 - int(tile_size*0.98)
            return self.w.create_polygon(
                x1, y1, x2, y2, x3, y3, fill="blue")

    def _draw_dir_right(self, x, y, right):
        tile_size = self.windowSize/self.max_dim
        x0, y0 = self._map_coords(x, y)
        if right:
            x1 = x0 + int(tile_size*0.98)
            y1 = y0 - int(tile_size*0.5)
            x2 = x0 + int(tile_size*0.85)
            y2 = y0 - int(tile_size*0.4)
            x3 = x0 + int(tile_size*0.85)
            y3 = y0 - int(tile_size*0.6)
            return self.w.create_polygon(
                x1, y1, x2, y2, x3, y3, fill="blue")

    def _draw_dir_down(self, x, y, down):
        tile_size = self.windowSize/self.max_dim
        x0, y0 = self._map_coords(x, y)
        if down:
            x1 = x0 + int(tile_size*0.4)
            y1 = y0 - int(tile_size*0.15)
            x2 = x0 + int(tile_size*0.6)
            y2 = y0 - int(tile_size*0.15)
            x3 = x0 + int(tile_size*0.5)
            y3 = y0 - int(tile_size*0.02)
            return self.w.create_polygon(
                x1, y1, x2, y2, x3, y3, fill="blue")

    def _draw_dir_left(self, x, y, left):
        tile_size = self.windowSize/self.max_dim
        x0, y0 = self._map_coords(x, y)
        if left:
            x1 = x0 + int(tile_size*0.02)
            y1 = y0 - int(tile_size*0.5)
            x2 = x0 + int(tile_size*0.15)
            y2 = y0 - int(tile_size*0.4)
            x3 = x0 + int(tile_size*0.15)
            y3 = y0 - int(tile_size*0.6)
            return self.w.create_polygon(
                x1, y1, x2, y2, x3, y3, fill="blue")

    def _draw_exit_point(self, x, y):
        """
        Draws exit_point as black square on top of
        """
        tile_size = self.windowSize/self.max_dim
        x0, y0 = self._map_coords(x, y)
        return self.w.create_rectangle(x0 + tile_size * 0.2,
                                       y0 - tile_size * 0.2,
                                       x0 + tile_size * 0.8,
                                       y0 - tile_size * 0.8,
                                       fill="purple")
    def _draw_shelf(self, x, y):
        """
        Draw shelf as small rectangle with character on top of it
        Characters should be unique in order to recognize
        what is going on during simulation
        """
        tile_size = self.windowSize/self.max_dim
        x0, y0 = self._map_coords(x, y)
        return self.w.create_rectangle(x0 + tile_size * 0.35,
                                       y0 - tile_size * 0.35,
                                       x0 + tile_size * 0.65,
                                       y0 - tile_size * 0.65,
                                       fill="orange")

    def _draw_shelf_name(self, x, y, name):
        tile_size = self.windowSize/self.max_dim
        x0, y0 = self._map_coords(x, y)
        return self.w.create_text(x0 + tile_size*0.5,
                                  y0 - tile_size*0.5,
                                  anchor=NW,
                                  text=name)

    def update(self, room, robots):
        # Redraw all elements in magazine that can move
        # Does not take into account that most of things
        # does not move at all
        # CAUTION!
        #     there is a bug!
        #     when exit point or shelf is added
        #     the direction is not deleted
        # FIXED
        # Preferred behaviour:
        # (1) Redraw only those elements that changed position
        # (2) make robots move smoothly
        # (3) make it pretty

        # Delete all existing robots.
        if self.robots:
            for robot in self.robots:
                self.w.delete(robot)
                self.master.update_idletasks()
        # Delete all existing robotDirections
        if self.robotsDirections:
            for dir_ in self.robotsDirections:
                self.w.delete(dir_)
                self.master.update_idletasks()
        # Delete all existing main roads
        if self.tilesDirections:
            for dir_ in self.tilesDirections:
                self.w.delete(dir_)
                self.master.update_idletasks()
        # Delete all exit points
        if self.exit_points:
            for exit_point in self.exit_points:
                self.w.delete(exit_point)
                self.master.update_idletasks()
        # Delete all shelfs
        if self.shelfs:
            for shelf in self.shelfs:
                self.w.delete(shelf)
                self.master.update_idletasks()
        # Delete all shelfs_names
        if self.shelfs_names:
            for name in self.shelfs_names:
                self.w.delete(name)
                self.w.update_idletasks()

        self.robots = []
        self.robotsDirections = []
        self.tilesDirections = []
        self.exit_points = []
        self.shelfs = []
        self.shelfs_names = []

        for exit_point in room.get_exit_points():
            self.exit_points.append(self._draw_exit_point(exit_point[0],
                                                          exit_point[1]))
        for robot in robots:
            self.robots.append(
                self._draw_robot(robot))
            self.robotsDirections.append(self._draw_robot_up(robot))
            self.robotsDirections.append(self._draw_robot_right(robot))
            self.robotsDirections.append(self._draw_robot_down(robot))
            self.robotsDirections.append(self._draw_robot_left(robot))

        for i in range(room.get_width()):
            for j in range(room.get_height()):
                if room.tiles[i][j].get_direction().get_up():
                    self.tilesDirections.append(self._draw_dir_up(
                        room.tiles[i][j].get_x(),
                        room.tiles[i][j].get_y(),
                        room.tiles[i][j].get_direction().get_up()))
                if room.tiles[i][j].get_direction().get_right():
                    self.tilesDirections.append(self._draw_dir_right(
                        room.tiles[i][j].get_x(),
                        room.tiles[i][j].get_y(),
                        room.tiles[i][j].get_direction().get_right()))
                if room.tiles[i][j].get_direction().get_down():
                    self.tilesDirections.append(self._draw_dir_down(
                        room.tiles[i][j].get_x(),
                        room.tiles[i][j].get_y(),
                        room.tiles[i][j].get_direction().get_down()))
                if room.tiles[i][j].get_direction().get_left():
                    self.tilesDirections.append(self._draw_dir_left(
                        room.tiles[i][j].get_x(),
                        room.tiles[i][j].get_y(),
                        room.tiles[i][j].get_direction().get_left()))

        for shelf in room.get_shelf_list():
            self.shelfs.append(self._draw_shelf(shelf.get_x(),
                                                shelf.get_y()))
            self.shelfs_names.append(self._draw_shelf_name(shelf.get_x(),
                                                           shelf.get_y(),
                                                           shelf.get_name()))

        # Update text
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(
            25, 0, anchor=NW,
            text=self._status_string(self.time))
        self.master.update()
        time.sleep(self.delay)

    def done(self):
        """
        Indicate that the animation is done so that we allow the user to close the window.
        """
        mainloop()