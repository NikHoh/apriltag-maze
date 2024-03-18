# Craft a maze from lasercut MDF walls and generate the corresponding AprilTag Bundle YAML
Code to craft (lasercut) a wooden maze, whose walls are engraved with AprilTags (https://github.com/AprilRobotics/apriltag) and generate the according  tag_bundle.yaml for the AprilTag detection library.

3D plot of exemplary maze            |  Exemplary real maze 
:-------------------------:|:-------------------------:
<img src="https://github.com/NikHoh/apriltag-maze/blob/main/maze_setup/images/plot_maze.png" width="438" height="337" />  |  <img src="https://github.com/NikHoh/apriltag-maze/blob/main/maze_setup/images/image_maze.png" width="438" height="242" />

## Craft a maze

Corresponding code in folder `maze_craft`.

A maze consists of MDF walls (250mm x 170mm x 3mm). Each wall consists of 4 AprilTags. One big and one small AprilTag on each side. 

Looking from above on a maze, the coordinate system origin is in the upper left corner with the x-axis pointing downwards and the y-axis pointing to the right.

By convention, the smallest AprilTag ID on a wall is a multiple of 4. It belongs to the big AprilTag that by convention and by default either points to North (on a horizontal wall) or to West (on a vertical wall). The small tag on the same side of the wall has ID +1. If there are tags on the other side, the big tag on the other side of the wall (pointing South or East) has ID +2. The small tag in the other side has ID +3.

Get png data of AprilTag family from https://github.com/AprilRobotics/apriltag-imgs and place it in the folder `tagCustom48h12`

Use `process_tags.py` to convert png tags into svg data (internally uses `tag_to_svg.py`).

Use `create_plate_for_laser.py` to create a svg file to lasercut a large MDF plate (1100mm x 550mm) that contains. Adapting the `tag_numbers` and setting `front = False`, the svg file for the respective back of the MDF plate can be generated.

The svg files are stored to the folder `final_plates_to_laser`.

The described pipline to generate svg data for a lasercutter are rather tailored (hardcoded) to the described plate and wall dimensions. If you want to adapt these, you will have to adapt the code in `create_plate_for_laser.py` and also the `sample_*_empty.svg` data in `maze_craft/do_not_touch`. The files `*backup.svg` can be ignored. To create a new `sample_*_empty.svg`, the files `sample_hinten.svg` and `sample_vorne.svg` were manually created and then the respective lines of code that describe the tags were removed manually.

If you also want to change the AprilTag dimensions, you will also have to adapt the file `process_tags.py`.

## Setup a maze

Corresponding code in folder `setup_maze`.

In a command window run `python maze_builder.py` (Python 3) and follow the instructions on the screen. The program will read in the AprilTags IDs of your current maze configuration, plot it, and save the corresponding tags.yaml file, which is used by the AprilTag Detection to localize with respect to the maze, in the folder `output`.

An exemplary command line input, which generates the maze seen in the picture above, is:

[Exemplary command line input](https://github.com/NikHoh/apriltag-maze/blob/main/maze_setup/images/console_example.png)

The described pipeline to generate the yaml data for a specific maze configuration is coded adaptively. If you want to adapt parameters like the size of walls or the space between walls, you can simply adapt them in the `class Wall` in `wall.py` (e.g. parameters `width`, `height`, and `thickness`) and the `class Maze` in  `maze.py` (e.g. parameters `offset_to_ground` and `space_between_walls`).

Have fun!




