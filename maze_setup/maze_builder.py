from maze import Maze
from typing import Optional
from typing import List

def new_line():
    print("")

def border_line():
    print("-------------------------------------------------------")

def get_positive_interger_input(message:str) -> int:
    """Asks for a user input being a positive integer"""
    while True:
        user_input = input(message)
        try:
            user_input = int(user_input)
        except ValueError:
            print("Your input must be a positive integer")
        if user_input <= 0:
            print("Your input must be a positive integer")
        else:
            break
    return user_input

def get_wall_id_input(message:str) -> List[int]:
    """Asks for a user input being space separated integers that are expected to be non-negative and even"""
    user_input = None
    while True:
        try:
            user_input = input(message)
            if "." in user_input or "," in user_input:
                print("You must not use commas for separation (only space) and no float values are permitted")
                continue
            user_input = [int(x) for x in user_input.split()]
        except ValueError:
            print("Your input must be positive even integers separated by a space (e.g. 2 64 6 10")
            continue
        if len(user_input) == 0:
            print("User input must not be empty.")
            continue
        all_valid = True
        for val in user_input:
            if val == -1:
                continue
            if val % 2 != 0 or val < -1:
                print("Your input must be positive even integers separated by a space (e.g. 2 64 6 10")
                all_valid = False
                break
        if all_valid:
            break
        else:
            continue
    if not isinstance(user_input, list):
        assert 1 == 0, "Something went wrong"
    return user_input




class MazeBuilder(object):
    def __init__(self):
        self.maze: Optional[Maze] = None

    def init_maze(self):
        self.maze = Maze()


    def get_maze_parameters_from_user(self):
        print("Hi, I am the Maze Builder, that helps you generate a AprilTag Tag Bundle YAML file that fits your maze "
              "configuration.")
        border_line()
        print("Following assumptions are made:")
        print("Looking from above on the maze, the coordinate system frame in in the top left of the maze.")
        print("The x axis is pointing downwards, the y axis is pointing to the right")
        print("The maze consists of walls.")
        print("A wall is assumed to have two AprilTags on the front (one big, one small) and two AprilTags on the back "
              "(again one big and one small)")
        print("The four IDs of the four AprilTags on one wall are always sequential and start with an even integer that "
              "is a multiple of 4, e.g.,"
              "4,5,6,7 are the four IDs on a wall.")
        print("When I ask you for the ID of a wall, I only need the smallest (and thus even) ID on the wall.")
        border_line()
        print("Important: Looking from the bird's perspective on the maze, I assume that the tag with the smallest ID "
              "on the wall either 'looks' up (in negative x direction) or 'looks' left (in negative y direction)")
        border_line()
        print("Let's start building your maze.")
        num_rows = get_positive_interger_input("How many rows (in x direction) does your maze have?")
        self.maze.set_number_of_rows(num_rows)
        num_cols = get_positive_interger_input("How many columns (in y direction) does your maze have?")
        self.maze.set_number_of_columns(num_cols)

        while True:
            self.get_maze_ids_from_user()
            if self.maze.check_input():
                break
            print("The user input of tag IDs was not correct. Try again.")

        self.maze.create_walls()

        self.maze.simple_plot()

        self.maze.advanced_plot()



    def get_maze_ids_from_user(self):
        print("In the following, give the tag IDs of a row of horizontal walls and then of a row of vertial walls, "
              "until all tags are given. Only use the smallest ID on a wall. Make sure the tag either faces upwards or "
              "to the left. If there is no wall at a position where a wall could be use -1")
        print("Looking from the bird's perspective we begin with the tag in the left upper corner")
        tag_ids_horizontal_walls = []
        tag_ids_vertical_walls = []
        for idx in range(0, max(self.maze.number_of_rows_horizontal_walls, self.maze.number_of_rows_vertical_walls)):
            if idx < self.maze.number_of_rows_horizontal_walls:
                while True:
                    user_input = get_wall_id_input(
                        f"Looking at the row of horizontal walls no. {idx + 1}, name the smallest ID on every "
                        "wall (it should look upwards) going from left to right. (-1 for missing wall)")
                    if len(user_input) != self.maze.num_horizontal_walls_per_row:
                        print(
                            f"According to the given size of the maze the number of given IDs and -1s must be {self.maze.num_horizontal_walls_per_row}.")
                    else:
                        break
                tag_ids_horizontal_walls.append(user_input)

            if idx < self.maze.number_of_rows_vertical_walls:
                while True:
                    user_input = get_wall_id_input(
                        f"Looking at the row of vertical walls no. {idx + 1}, name the smallest ID on every "
                        "wall (it should look to the left) going from left to right. (-1 for missing wall)")
                    if len(user_input) != self.maze.num_vertical_walls_per_row:
                        print(
                            f"According to the given size of the maze the number of given IDs and -1s must be {self.maze.num_vertical_walls_per_row}.")
                    else:
                        break
                tag_ids_vertical_walls.append(user_input)

        self.maze.rows_with_horizontal_walls = tag_ids_horizontal_walls
        self.maze.rows_with_vertical_walls = tag_ids_vertical_walls

    def save_yaml(self):
        pass
        



def main():
    maze_builder = MazeBuilder()
    maze_builder.init_maze()
    maze_builder.get_maze_parameters_from_user()
    maze_builder.save_yaml()
    print("End of program. Thanks and see you soon.")



if __name__ == '__main__':
    main()