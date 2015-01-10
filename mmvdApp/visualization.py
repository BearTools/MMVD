# coding: utf-8
__author__ = 'wojciech'

import time
from Tkinter import *


class Visualization(Frame):
    def __init__(self, map_):
        self.master = Tk()
        Frame.__init__(self, self.master)

        self.magazine_frame = Frame(self.master)
        self.magazine_frame.pack(side=LEFT)

        self.control_frame = Frame(self.master)
        self.control_frame.pack()
        self.magazine_len = 500  # szerokosc magazynu
        self.magazine_len = 500  # wysokosc magazynu

        self.x_dim = len(map_)  # wymiar x
        self.y_dim = len(map_[0])  # wymiar y
        self.max_dim = max(self.y_dim, self.x_dim)

        self.robotspeed = 10
        self.robot_number = 0

        self.tile_len = self.magazine_len / self.max_dim
        self.canvas = Canvas(self.magazine_frame, width=self.magazine_len,
                             height=self.magazine_len)

        speed_scale = Scale(self.control_frame,
                            from_=1,
                            to=100,
                            # variable=10,
                            orient=HORIZONTAL,
                            length=200,
                            label="Robot speed",
                            sliderlength=20,
                            command=self.speed_scale_command)
        speed_scale.set(10)
        speed_scale.pack()
        stop_button = Button(self.control_frame,
                             text="STOP",
                             command=self.end,
                             borderwidth=3)
        stop_button.pack()

        self.variable = StringVar(self.master)
        self.variable.set("500x500")

        self.w = OptionMenu(self.master, self.variable, "100x100", "200x200",
                            "300x300", "400x400", "500x500", "600x600",
                            "700x700", "800x800", "900x900")
        self.w.pack()

        self.canvas.pack()

        # Start of drawing magazine.
        # Tiles are drawn first, they are on the bottom of magazine
        # It is nor recommended to move around tiles but if it is necessary
        # Tiles can be accessed by their position starting form (0,0)
        for i in range(len(map_)):
            for j in range(len(map_[i])):
                self.canvas.create_rectangle(self.tile_len * j,
                                             self.tile_len * i,
                                             self.tile_len * j + self.tile_len,
                                             self.tile_len * i + self.tile_len,
                                             fill="grey",
                                             tag="tile" + str(j) + str(i))
                self.canvas.update()

        # Draws all directions according to the map given to the algorithm
        # Tiles can be accessed by their position starting form (0,0)
        for i in range(len(map_)):
            for j in range(len(map_[i])):
                # double arrow in the up direction
                if map_[i][j] == 1:
                    self.canvas.create_line(
                        self.tile_len * j + 0.35 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.15,
                        self.tile_len * j + 0.5 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.05,
                        self.tile_len * j + 0.65 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.15,
                        fill="darkgreen", width=4, tag="dir" + str(j) + str(i)
                    )
                    self.canvas.create_line(
                        self.tile_len * j + 0.35 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.25,
                        self.tile_len * j + 0.5 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.15,
                        self.tile_len * j + 0.65 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.25,
                        fill="darkgreen", width=4, tag="dir" + str(j) + str(i)
                    )

                # Double arrow in the right direction
                elif map_[i][j] == 2:
                    self.canvas.create_line(
                        self.tile_len * j + 0.85 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.35,
                        self.tile_len * j + 0.95 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.5,
                        self.tile_len * j + 0.85 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.65,
                        fill="darkgreen", width=4, tag="dir" + str(j) + str(i)
                    )
                    self.canvas.create_line(
                        self.tile_len * j + 0.75 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.35,
                        self.tile_len * j + 0.85 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.5,
                        self.tile_len * j + 0.75 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.65,
                        fill="darkgreen", width=4, tag="dir" + str(j) + str(i)
                    )

                # Double arrow in the down direction
                elif map_[i][j] == 3:
                    self.canvas.create_line(
                        self.tile_len * j + 0.35 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.85,
                        self.tile_len * j + 0.5 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.95,
                        self.tile_len * j + 0.65 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.85,
                        fill="darkgreen", width=4, tag="dir" + str(j) + str(i)
                    )
                    self.canvas.create_line(
                        self.tile_len * j + 0.35 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.75,
                        self.tile_len * j + 0.5 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.85,
                        self.tile_len * j + 0.65 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.75,
                        fill="darkgreen", width=4, tag="dir" + str(j) + str(i)
                    )

                # Double arrow in the left direction
                elif map_[i][j] == 4:
                    self.canvas.create_line(
                        self.tile_len * j + 0.15 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.35,
                        self.tile_len * j + 0.05 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.5,
                        self.tile_len * j + 0.15 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.65,
                        fill="darkgreen", width=4, tag="dir" + str(j) + str(i)
                    )
                    self.canvas.create_line(
                        self.tile_len * j + 0.25 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.35,
                        self.tile_len * j + 0.15 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.5,
                        self.tile_len * j + 0.25 * self.tile_len,
                        self.tile_len * i + self.tile_len * 0.65,
                        fill="darkgreen", width=4, tag="dir" + str(j) + str(i)
                    )

                # Exit point as a big dotted X
                elif map_[i][j] == 9:
                    self.canvas.create_polygon(
                        self.tile_len * j + 0.12 * self.tile_len,
                        self.tile_len * i + 0.21 * self.tile_len,
                        self.tile_len * j + 0.21 * self.tile_len,
                        self.tile_len * i + 0.12 * self.tile_len,
                        self.tile_len * j + 0.5 * self.tile_len,
                        self.tile_len * i + 0.4 * self.tile_len,
                        self.tile_len * j + 0.79 * self.tile_len,
                        self.tile_len * i + 0.12 * self.tile_len,
                        self.tile_len * j + 0.88 * self.tile_len,
                        self.tile_len * i + 0.21 * self.tile_len,
                        self.tile_len * j + 0.6 * self.tile_len,
                        self.tile_len * i + 0.5 * self.tile_len,
                        self.tile_len * j + 0.88 * self.tile_len,
                        self.tile_len * i + 0.79 * self.tile_len,
                        self.tile_len * j + 0.79 * self.tile_len,
                        self.tile_len * i + 0.88 * self.tile_len,
                        self.tile_len * j + 0.5 * self.tile_len,
                        self.tile_len * i + 0.6 * self.tile_len,
                        self.tile_len * j + 0.21 * self.tile_len,
                        self.tile_len * i + 0.88 * self.tile_len,
                        self.tile_len * j + 0.12 * self.tile_len,
                        self.tile_len * i + 0.79 * self.tile_len,
                        self.tile_len * j + 0.4 * self.tile_len,
                        self.tile_len * i + 0.5 * self.tile_len,
                        fill="darkred", outline="black", stipple='gray75',
                        width=3)

                else:
                    self.canvas.create_rectangle(
                        self.tile_len * j + 0.25 * self.tile_len,
                        self.tile_len * i + 0.25 * self.tile_len,
                        self.tile_len * j + 0.75 * self.tile_len,
                        self.tile_len * i + 0.75 * self.tile_len,
                        fill="red", tag="shelf" + map_[i][j],
                    )
                    self.canvas.create_text(
                        self.tile_len * j + 0.5 * self.tile_len,
                        self.tile_len * i + 0.5 * self.tile_len,
                        anchor="center", text=map_[i][j],
                        tag="shelf_text" + map_[i][j]
                    )

                self.canvas.update()

    def draw_robots(self, robot_list):
        """
        Function draws a new robot
        It should be used to introduce robots to magazine
        Robots are given id that are used to access robot
        Id is the position of the robot on robot_list
        starting with 0
        :param robot_list: List of robots
        :return: None
        """

        for robot in robot_list:
            self.canvas.create_oval(
                robot[0] * self.tile_len + self.tile_len * 0.2,
                robot[1] * self.tile_len + self.tile_len * 0.2,
                robot[0] * self.tile_len + self.tile_len * 0.8,
                robot[1] * self.tile_len + self.tile_len * 0.8,
                fill="blue", tag="robot" + str(self.robot_number)
            )
            self.robot_number += 1

    def hide_shelf(self, shelf_id):
        """
        Removes shelf with shelf_id from view.
        Shelf is not removed from memory.
        When moved appears in the magazine
        :param shelf_id: name of shelf to be hidden
        :return:
        """
        self.canvas.lower("shelf" + shelf_id)
        self.canvas.lower("shelf_text" + shelf_id)

    def animate(self, update_robots, update_shelfs):
        """
        Function makes smooth moves of robots and shelfs in the magazine
        Function assumes that both x_len and y_len are the same
        :param update_robots: List of all robots positions to be updated
            it is a list that has at the first position Id of robot to
            be updated(generated with draw robots function),
            second number indicates direction

            Assumes that movement to be executed is a valid movement
            Assumes that all robots exist
        :param update_shelfs: List of all shelfs to be updated
            each element to lis has at the first position shelf name (Id) of
            shelf to be updated, second number indicates direction
            0- hide shelf

            Assume that movement to be executed is a valid movement
            Assume that all shelfs exist
            If hidden shelf is moved it shows up in the magazine
        :return: None
        """

        for i in range(self.tile_len):
            time.sleep(.05/self.robotspeed)
            for shelf in update_shelfs:
                horizontal = 0
                vertical = 0
                if shelf[1] == 1:
                    vertical = -1
                elif shelf[1] == 2:
                    horizontal = 1
                elif shelf[1] == 3:
                    vertical = 1
                elif shelf[1] == 4:
                    horizontal = -1
                if shelf[1] == 0:
                    self.hide_shelf(shelf[0])
                else:
                    self.canvas.move('shelf' + shelf[0], horizontal, vertical)
                    self.canvas.move('shelf_text' + shelf[0], horizontal,
                                     vertical)
                    self.canvas.tag_raise("shelf"+shelf[0])
                    self.canvas.tag_raise("shelf_text"+shelf[0])

            for robot in update_robots:
                horizontal = 0
                vertical = 0
                if robot[1] == 1:
                    vertical = -1
                elif robot[1] == 2:
                    horizontal = 1
                elif robot[1] == 3:
                    vertical = 1
                elif robot[1] == 4:
                    horizontal = -1
                self.canvas.move('robot' + str(robot[0]), horizontal, vertical)
            self.canvas.update()
            # time.clock().
        self.resize_magazine(self.variable.get())
        time.sleep(0.5/self.robotspeed)

    def speed_scale_command(self, value):
        self.robotspeed = int(value)

    def end(self):
        self.mainloop()

    def resize_magazine(self, val):
        if val == "100x100":
            self.canvas.scale("all", 0, 0, 100. / self.magazine_len,
                              100. / self.magazine_len)
            self.magazine_len = 100
            self.magazine_len = 100
            self.tile_len = self.magazine_len/self.x_dim
            self.tile_len = self.magazine_len/self.y_dim
            self.canvas.config(width=self.magazine_len,
                               height=self.magazine_len)
        elif val == "200x200":
            self.canvas.scale("all", 0, 0, 200. / self.magazine_len,
                              200. / self.magazine_len)
            self.magazine_len = 200
            self.magazine_len = 200
            self.tile_len = self.magazine_len/self.x_dim
            self.tile_len = self.magazine_len/self.y_dim
            self.canvas.config(width=self.magazine_len,
                               height=self.magazine_len)
        elif val == "300x300":
            self.canvas.scale("all", 0, 0, 300. / self.magazine_len,
                              300. / self.magazine_len)
            self.magazine_len = 300
            self.magazine_len = 300
            self.tile_len = self.magazine_len/self.x_dim
            self.tile_len = self.magazine_len/self.y_dim
            self.canvas.config(width=self.magazine_len,
                               height=self.magazine_len)
        elif val == "400x400":
            self.canvas.scale("all", 0, 0, 400. / self.magazine_len,
                              400. / self.magazine_len)
            self.magazine_len = 400
            self.magazine_len = 400
            self.tile_len = self.magazine_len/self.x_dim
            self.tile_len = self.magazine_len/self.y_dim
            self.canvas.config(width=self.magazine_len,
                               height=self.magazine_len)
        elif val == "500x500":
            self.canvas.scale("all", 0, 0, 500. / self.magazine_len,
                              500. / self.magazine_len)
            self.magazine_len = 500
            self.magazine_len = 500
            self.tile_len = self.magazine_len/self.x_dim
            self.tile_len = self.magazine_len/self.y_dim
            self.canvas.config(width=self.magazine_len,
                               height=self.magazine_len)
        elif val == "600x600":
            self.canvas.scale("all", 0, 0, 600. / self.magazine_len,
                              600. / self.magazine_len)
            self.magazine_len = 600
            self.magazine_len = 600
            self.tile_len = self.magazine_len/self.x_dim
            self.tile_len = self.magazine_len/self.y_dim
            self.canvas.config(width=self.magazine_len,
                               height=self.magazine_len)
        elif val == "700x700":
            self.canvas.scale("all", 0, 0, 700. / self.magazine_len,
                              700. / self.magazine_len)
            self.magazine_len = 700
            self.magazine_len = 700
            self.tile_len = self.magazine_len/self.x_dim
            self.tile_len = self.magazine_len/self.y_dim
            self.canvas.config(width=self.magazine_len,
                               height=self.magazine_len)
        elif val == "800x800":
            self.canvas.scale("all", 0, 0, 800. / self.magazine_len,
                              800. / self.magazine_len)
            self.magazine_len = 800
            self.magazine_len = 800
            self.tile_len = self.magazine_len/self.x_dim
            self.tile_len = self.magazine_len/self.y_dim
            self.canvas.config(width=self.magazine_len,
                               height=self.magazine_len)
        elif val == "900x900":
            self.canvas.scale("all", 0, 0, 900. / self.magazine_len,
                              900. / self.magazine_len)
            self.magazine_len = 900
            self.magazine_len = 900
            self.tile_len = self.magazine_len/self.x_dim
            self.tile_len = self.magazine_len/self.y_dim
            self.canvas.config(width=self.magazine_len,
                               height=self.magazine_len)
