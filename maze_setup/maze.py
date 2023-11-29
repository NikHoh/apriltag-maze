from typing import Optional
from typing import List
from wall import Wall
from wall import Placement

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
        3. Only even non-negative wall IDs or -1
        4. No repitions in tag IDs
        5. Tag IDs are multiples of 4
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
            if val >= 0:
                if val % 2 != 0:
                    print("IDs must be even")
                    everything_okay = False
                if val % 4 != 0:
                    print("IDs must be multiples of 4 (look at the assumptions).")
                    everything_okay = False
            else:
                if val != -1:
                    print("If there is no wall -1 must be given")
                    everything_okay = False
        return everything_okay

    def create_walls(self):
        wall = Wall()
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








