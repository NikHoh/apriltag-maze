from maze import Maze
from typing import Optional
from typing import List
import os
from wall import Tag
from wall import Orientation

def new_line():
    print("")

def border_line():
    print("-------------------------------------------------------")

def read_yaml_file(path:str) -> str:
    """Reads in text from a path"""
    assert os.path.isfile(path), f"Given path {path} does not exist"
    with open(path) as f:
        s = f.read()
    return s

def save_yaml_file(string_to_save:str, path:str):
    """Writes text to a path"""
    assert not os.path.isfile(path), "Filename that you want to use to save already exits. Choose another one."
    with open(path, 'w') as f:
        f.write(string_to_save)

def replace_string_in_string(complete_string:str, old_string:str, new_string:str) -> str:
    """Replaces a text within a string"""
    assert old_string in complete_string, f"Expected string {old_string} not found in complete string"
    return complete_string.replace(old_string, new_string)

def get_yaml_line_for(tag: Tag, last_tag=False) -> str:
    if tag.size.x == 140:
        size = "0.084"   # the yaml file takes the inner size of the tag in m
    elif tag.size.x == 28:
        size = "0.0168"  # the yaml file takes the inner size of the tag in m
    else:
        assert 1 == 0, f"Tag size {tag.size} not known."
    id = tag.tag_id
    x = tag.position.x/1000  # tag file takes position in m
    y = tag.position.y/1000  # tag file takes position in m
    z = tag.position.z/1000  # tag file takes position in m

    if tag.orientation == Orientation.NORTH:
        orientation_string = "qw: 0.5, qx: 0.5, qy: -0.5, qz: -0.5"
    elif tag.orientation == Orientation.WEST:
        orientation_string = "qw: 0.7071068, qx: 0.7071068, qy: 0, qz: 0"
    elif tag.orientation == Orientation.SOUTH:
        orientation_string = "qw: 0.5, qx: 0.5, qy: 0.5, qz: 0.5"
    elif tag.orientation == Orientation.EAST:
        orientation_string = "qw: 0, qx: 0, qy: 0.7071068, qz: 0.7071068"
    else:
        assert 1 == 0, "Unknown orientation"

    tag_string = f"{{id: {id}, size: {size}, x: {x}, y: {y}, z: {z}, {orientation_string}}}"
    if last_tag:
        tag_string += "\n"
    else:
        tag_string += ",\n"

    return tag_string

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
    """Asks for a user input being space separated integers that are expected to be even, or -1 (special case)."""
    user_input = None
    while True:
        try:
            user_input = input(message)
            if "-0" in user_input:
                print("The wall with tag ID 0 is a special case that is not allowed to look downwards or right. Please flip the wall.")
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
            if val % 2 != 0:
                print("Your input must be even (or -1) integers separated by a space (e.g. 2 -1 -6 10")
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
        print("A wall is assumed to have two AprilTags on the front (one big, one small) and optionally two AprilTags on the back "
              "(again one big and one small)")
        print("The big tag on one side has always an even ID.")
        print("When I ask you for the ID of a wall, I only need the smallest (and even) ID on the wall.")
        border_line()
        print("Important: Looking from the bird's perspective on the maze, I assume that the tag with the smallest ID "
              "on the wall either 'looks' up (in negative x direction called NORTH) or 'looks' left (in negative y direction called WEST)")
        print("If you want to me to flip the wall, e.g. the smallest tag ID looking to the right or down, then you previx the ID with a Minus (e.g. -4 instead of 4).")
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
              "until all tags are given. Only use the smallest ID on a wall. If the smallest tag either faces upwards or "
              "to the left, you give me the pure tag ID, else you give me the negative tag ID. If there is no wall at a position where a wall could be use -1")
        print("Looking from the bird's perspective we begin with the tag in the left upper corner")
        tag_ids_horizontal_walls = []
        tag_ids_vertical_walls = []
        for idx in range(0, max(self.maze.number_of_rows_horizontal_walls, self.maze.number_of_rows_vertical_walls)):
            if idx < self.maze.number_of_rows_horizontal_walls:
                while True:
                    user_input = get_wall_id_input(
                        f"Looking at the row of horizontal walls no. {idx + 1}, name the smallest ID on every "
                        "wall going from left to right. (-1 for missing wall)")
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
                        "wall going from left to right. (-1 for missing wall)")
                    if len(user_input) != self.maze.num_vertical_walls_per_row:
                        print(
                            f"According to the given size of the maze the number of given IDs and -1s must be {self.maze.num_vertical_walls_per_row}.")
                    else:
                        break
                tag_ids_vertical_walls.append(user_input)

        self.maze.rows_with_horizontal_walls = tag_ids_horizontal_walls
        self.maze.rows_with_vertical_walls = tag_ids_vertical_walls

    def save_maze_as_yaml(self):
        while True:
            while True:
                save_name = input("Type in name of YAML file (no spaces)")
                if " " in save_name:
                    print("No spaces in save_name allowed")
                else:
                    break
            if not ".yaml" in save_name:
                save_name += ".yaml"
            save_path = os.path.join(os.getcwd(), "output", save_name)

            if os.path.isfile(save_path):
                print("Name does already exist. Please choose other name.")
            else:
                break

        maze_yaml_text = ""

        for wall_idx, wall in enumerate(self.maze.walls):
            for tag_idx, tag in enumerate(wall.tags):
                maze_yaml_text += get_yaml_line_for(tag, last_tag=(wall_idx==len(self.maze.walls)-1 and tag_idx == len(wall.tags)-1))

        file_content = read_yaml_file(os.path.join(os.getcwd(), "do_not_touch", "empty_tags.yaml"))

        file_content = replace_string_in_string(file_content, "add_tag_description_here", maze_yaml_text)

        save_yaml_file(file_content, save_path)

        print(f"Maze yaml file was saved to {save_path}.")



def main():
    maze_builder = MazeBuilder()
    maze_builder.init_maze()
    maze_builder.get_maze_parameters_from_user()
    maze_builder.save_maze_as_yaml()
    print("End of program. Thanks and see you soon.")



if __name__ == '__main__':
    main()