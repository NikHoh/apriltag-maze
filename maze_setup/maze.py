from typing import Optional
from typing import List
from wall import Wall
from wall import Placement
import math



class Maze(object):
    def __init__(self):
        self.offset_to_ground = 3 # mm
        self.space_between_walls = 3 # mm
        self.number_of_rows: Optional[int] = None
        self.number_of_columns: Optional[int] = None
        self.number_of_rows_vertical_walls: Optional[int] = None
        self.number_of_rows_horizontal_walls: Optional[int] = None

        self.num_horizontal_walls_per_row = None
        self.num_vertical_walls_per_row = None

        self.rows_with_horizontal_walls: Optional[List[List[int]]] = None
        self.rows_with_vertical_walls: Optional[List[List[int]]] = None

        self.walls: Optional[List[Wall]] = []

    def set_number_of_rows(self, num_rows:int):
        self.number_of_rows = num_rows
        self.update_num_rows()

    def set_number_of_columns(self, num_cols):
        self.number_of_columns = num_cols
        self.update_num_walls_per_row()

    def update_num_walls_per_row(self):
        self.num_horizontal_walls_per_row = self.number_of_columns
        self.num_vertical_walls_per_row = self.number_of_columns + 1

    def update_num_rows(self):
        self.number_of_rows_vertical_walls = self.number_of_rows
        self.number_of_rows_horizontal_walls = self.number_of_rows + 1

    def check_input(self) -> bool:
        """When this function is called, the input of the maze is assumed to be finished. This function checks for
        correct input that is
        1. Correct number of rows
        2. Correct number of walls per rows
        3. Only even wall IDs or -1
        4. No repitions in tag IDs
        """
        everything_okay = True
        if not len(self.rows_with_horizontal_walls) == self.number_of_rows_horizontal_walls:
            everything_okay = False
            print("Number of rows with horizontal walls does not fit maze size")
        if not len(self.rows_with_vertical_walls) == self.number_of_rows_vertical_walls:
            everything_okay = False
            print("Number of rows with vertical walls does not fit maze size")
        if not self.check_row_of_walls(self.rows_with_horizontal_walls, self.num_horizontal_walls_per_row):
            everything_okay = False
        if not self.check_row_of_walls(self.rows_with_vertical_walls, self.num_vertical_walls_per_row):
            everything_okay = False
        used_ids = []
        for row in self.rows_with_horizontal_walls:
            for tag in row:
                if tag > -1:
                    used_ids.append(tag)
        for row in self.rows_with_vertical_walls:
            for tag in row:
                if tag > -1:
                    used_ids.append(tag)
        if not len(used_ids) == len(set(used_ids)):
            print("Each ID must only be there once.")
            everything_okay = False

        return everything_okay

    def check_row_of_walls(self, list_of_rows, expected_row_length):
        everything_okay = True
        for row in list_of_rows:
            if not len(row) == expected_row_length:
                everything_okay = False
                print("Number of walls in row walls does not fit maze size.")
            if not self.check_tag_id(row):
                everything_okay = False
        return everything_okay

    def check_tag_id(self, row):
        everything_okay = True
        for val in row:
            if val != -1:
                if val % 2 != 0:
                    print("IDs must be even")
                    everything_okay = False
        return everything_okay

    def create_walls(self):
        wall = Wall()
        assert wall.thickness == self.space_between_walls, "Wall thickness is assumed to equal the space_between_walls " \
                                                           "in the position calculations. Here they differ. " \
                                                           "No guarantee for proper results."
        for row_id, row in enumerate(self.rows_with_horizontal_walls):
            for tag_index, tag_id in enumerate(row):
                if tag_id == -1:
                    continue
                pos_y = self.space_between_walls + int(wall.width/2) + tag_index * (self.space_between_walls + wall.width)
                pos_x = row_id * (self.space_between_walls + wall.width)
                pos_z = self.offset_to_ground + int(wall.height / 2)
                self.walls.append(Wall(Placement.HORIZONTAL, pos_x = pos_x, pos_y=pos_y, pos_z=pos_z,
                                       smallest_tag_id=tag_id))

        for row_id, row in enumerate(self.rows_with_vertical_walls):
            for tag_index, tag_id in enumerate(row):
                if tag_id == -1:
                    continue
                pos_y = tag_index * (self.space_between_walls + wall.width)
                pos_x = self.space_between_walls + int(wall.width/2) + row_id * (self.space_between_walls + wall.width)
                pos_z = self.offset_to_ground + int(wall.height / 2)
                self.walls.append(Wall(Placement.VERTICAL, pos_x=pos_x, pos_y=pos_y, pos_z=pos_z,
                                       smallest_tag_id=tag_id))

    def simple_plot(self):
        print("Your maze should look like this.")
        print("")
        ksy_space = "          "
        ksy = " ---> y \n|\n|\nv\nx\n"
        maze_string = ""
        maze_string += ksy
        vert_wall = "|"
        hor_placeholder = " "
        hor_wall = "----"
        no_hor_wall = "    "
        no_vert_wall = " "
        vert_placeholder = "    "
        for idx in range(0, max(self.number_of_rows_horizontal_walls, self.number_of_rows_vertical_walls)):
            if idx < self.number_of_rows_horizontal_walls:
                maze_string += ksy_space
                maze_string += hor_placeholder
                for tag in self.rows_with_horizontal_walls[idx]:
                    if tag != -1:
                        maze_string += hor_wall
                    else:
                        maze_string += no_hor_wall
                    maze_string += hor_placeholder
                maze_string += "\n"

            if idx < self.number_of_rows_vertical_walls:
                maze_string += ksy_space
                for tag in self.rows_with_vertical_walls[idx]:
                    if tag != -1:
                        maze_string += vert_wall
                    else:
                        maze_string += no_vert_wall
                    maze_string += vert_placeholder
                maze_string += "\n"
        print(maze_string)


    def advanced_plot(self):
        user_input = input("Do you want a 3D plot of your maze (matplotlib package must be installed)? (y or n):")

        if user_input == "y":
            import matplotlib
            import matplotlib.pyplot as plt
            matplotlib.use('TkAgg')
            from matplotlib.patches import PathPatch
            from matplotlib.patches import Rectangle
            from matplotlib.text import TextPath
            from matplotlib.transforms import Affine2D
            import mpl_toolkits.mplot3d.art3d as art3d
            matlib_version = matplotlib.__version__.split(".")
            if int(matlib_version[0]) < 3 or (int(matlib_version[0]) == 3 and int(matlib_version[1]) < 8):
                print(f"Your matplotlib version is {matplotlib.__version__}")
                print("You need ad least matplotlib version 3.8.0.")
                print("Continue without 3D plot.")
                return

            def text3d(ax, xyz, s, zdir="z", size=None, angle=0, **kwargs):
                """
                Copyright: https://matplotlib.org/stable/gallery/mplot3d/pathpatch3d.html#sphx-glr-gallery-mplot3d-pathpatch3d-py
                Plots the string *s* on the axes *ax*, with position *xyz*, size *size*,
                and rotation angle *angle*. *zdir* gives the axis which is to be treated as
                the third dimension. *usetex* is a boolean indicating whether the string
                should be run through a LaTeX subprocess or not.  Any additional keyword
                arguments are forwarded to `.transform_path`.

                Note: zdir affects the interpretation of xyz.
                """
                x, y, z = xyz
                if zdir == "y":
                    xy1, z1 = (x, z), y
                    zdir = (0,1,0)
                elif zdir == "x":
                    xy1, z1 = (y, z), x
                    zdir = (1, 0, 0)
                elif zdir == "z":
                    xy1, z1 = (x, y), z
                    zdir = (0,0,1)
                else:
                    assert 1 == 0, "zdir not defined"

                text_path = TextPath((0, 0), s, size=size, usetex=False)
                trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])

                p1 = PathPatch(trans.transform_path(text_path), edgecolor="k", facecolor="k", **kwargs)
                ax.add_patch(p1)
                art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')

            ris_green = (0.0, 157/255, 129/255, 1.0) # RGBA
            cream = (209/255, 240/255, 177/255, 1.0) # RGBA
            light_blue = (0/255, 105/255, 146/255, 1.0) # RGBA
            dark_blue = (39/255, 71/255, 110/255, 1.0) # RGBA

            for wall in self.walls:
                # plot the side of the wall with the smallest id
                if wall.placement == Placement.HORIZONTAL:
                    r1 = Rectangle((wall.pos_y - (wall.width / 2),
                                   wall.pos_z - (wall.height / 2)),
                                   wall.width,
                                   wall.height,
                                   color=ris_green)
                    if wall.smallest_tag_id >= 0:
                        text3d(ax, (wall.pos_x-50, wall.pos_y, 0), str(wall.tags[0].tag_id), zdir="z", angle=-math.pi/2, size=40, zorder=10)
                    else:
                        text3d(ax, (wall.pos_x + 50, wall.pos_y, 0), str(wall.tags[0].tag_id), zdir="z",
                               angle=math.pi / 2, size=40, zorder=10)
                    r2 = Rectangle((wall.pos_y - (wall.width / 2),
                                    wall.pos_z - (wall.height / 2)),
                                   wall.width,
                                   wall.height,
                                   color=cream)
                    if len(wall.tags) > 2:
                        if wall.smallest_tag_id >= 0:
                            text3d(ax, (wall.pos_x+50, wall.pos_y, 0), str(wall.tags[2].tag_id), zdir="z", angle=math.pi/2, size=40, zorder=10)
                        else:
                            text3d(ax, (wall.pos_x - 50, wall.pos_y, 0), str(wall.tags[2].tag_id), zdir="z",
                                   angle=-math.pi / 2, size=40, zorder=10)
                elif wall.placement == Placement.VERTICAL:
                    r1 = Rectangle((wall.pos_x - (wall.width / 2),
                                    wall.pos_z - (wall.height / 2)),
                                   wall.width,
                                   wall.height,
                                   color=light_blue)
                    if wall.smallest_tag_id >= 0:
                        text3d(ax, (wall.pos_x, wall.pos_y-50, 0), str(wall.tags[0].tag_id), zdir="z", size=40, zorder=10)
                    else:
                        text3d(ax, (wall.pos_x, wall.pos_y + 50, 0), str(wall.tags[0].tag_id), zdir="z", angle=math.pi,
                               size=40, zorder=10)
                    r2 = Rectangle((wall.pos_x - (wall.width / 2),
                                    wall.pos_z - (wall.height / 2)),
                                   wall.width,
                                   wall.height,
                                   color=dark_blue)
                    if len(wall.tags) > 2:
                        if wall.smallest_tag_id >= 0:
                            text3d(ax, (wall.pos_x, wall.pos_y+50, 0), str(wall.tags[2].tag_id), zdir="z", angle=math.pi, size=40, zorder=10)
                        else:
                            text3d(ax, (wall.pos_x, wall.pos_y - 50, 0), str(wall.tags[2].tag_id), zdir="z", size=40,
                                   zorder=10)
                ax.add_patch(r1)
                ax.add_patch(r2)
                if wall.placement == Placement.HORIZONTAL:
                    art3d.pathpatch_2d_to_3d(r1, z=wall.pos_x, zdir="x")
                    art3d.pathpatch_2d_to_3d(r2, z=wall.pos_x+wall.thickness, zdir="x")
                elif wall.placement == Placement.VERTICAL:
                    art3d.pathpatch_2d_to_3d(r1, z=wall.pos_y, zdir="y")
                    art3d.pathpatch_2d_to_3d(r2, z=wall.pos_y + wall.thickness, zdir="y")
            x_size = (self.number_of_rows+1)*self.walls[0].width
            y_size = (self.number_of_columns+1)*self.walls[0].width
            z_size = int(self.walls[0].height*1.5)
            ax.set_xlim(0, x_size)
            ax.set_ylim(0, y_size)
            ax.set_zlim(0, z_size)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("z")

            ax.set_box_aspect((1, y_size/x_size, z_size/x_size))
            plt.show()









