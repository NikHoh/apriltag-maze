# Craft a maze from lasercut MDF walls and generate the corresponding AprilTag Bundle YAML
Code to craft (lasercut) a wooden maze, whose walls are engraved with AprilTags and generate the according  tag_bundle.yaml for the AprilTag detection library.

3D plot of examplary maze            |  Examplary real maze 
:-------------------------:|:-------------------------:
![3D plot of examplary maze](https://github.com/NikHoh/apriltag-maze/blob/main/maze_setup/images/plot_maze.png)  |  ![Examplary real maze](https://github.com/NikHoh/apriltag-maze/blob/main/maze_craft/images/real_maze.png)

## Craft a maze

Corresponding code in folder `maze_craft`.

A maze consists of MDF walls (250mm x 170mm x 3mm). Each wall consists of 4 AprilTags. One big and one small AprilTag on each side. 

Looking from abow on a maze, the coordinate system origin is in the upper left corner with the x-axis pointing downwards and the y-axis pointing to the right.

By convention, the smallest AprilTag ID on a wall is a multiple of 4. It belongs to the big AprilTag that by convention either points to North (on a horizontal wall) or to West (on a vertical wall). The small tag on the same side of the wall has ID +1. The big tag on the other side of the wall (pointing South or East) has ID +1. The small tag in the other side has ID +1.

Get png data of AprilTag family from https://github.com/AprilRobotics/apriltag-imgs and place it in the folder `tagCustom48h12`

Use `process_tags.py` to convert png tags into svg data (internally uses `tag_to_svg.py`).

Use `create_plate_for_laser.py` to create a svg file to lasercut a large MDF plate (1100mm x 550mm) that contains. Adapting the `tag_numbers` and setting `front = False`, the svg file for the respective back of the MDF plate can be generated.

The svg files are stored to the folder `final_plates_to_laser`.

## Setup a maze

Corresponding code in folder `setup_maze`.

In a command window run `python maze_builder.py` (Python 3) and follow the instructions on the screen. The program will read in the AprilTags IDs of your current maze configuration, plot it, and save the corresponding tags.yaml file, which is used by the AprilTag Detection to localize with respect to the maze, in the folder `output`.

An exmaplary command line input, which generates the maze seen in the picture above, is:

[Exemplary command line input](https://github.com/NikHoh/apriltag-maze/blob/main/maze_setup/images/console_example.png)

Have fun!




