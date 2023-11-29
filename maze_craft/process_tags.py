#!/usr/bin/env python3
import os

def main():
    """Loads tags (png) from AprilTag base folder from Repository
    and stores them as svg (even tags ids are stored as 140mm sized svg and uneven tag ids are stored as 28mm sized
    svg data in the folder named tags_scaled"""
    output_folder = "tags_scaled"
    output_folder_path = os.path.join(os.getcwd(), output_folder)
    input_folder = "tagCustom48h12"
    input_folder_path = os.path.join(os.getcwd(), input_folder)
    files_to_process = 500

    directory = os.fsencode(input_folder_path)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if not filename.endswith(".png"):
            continue
        else:
            filename_without_ending = filename.split(".png")[0]
            counter = int(filename.split("_12_")[1].split(".")[0])
            if counter < files_to_process:
                if counter%2 == 0:  # make large tag
                    output_filename = f"{filename_without_ending}_140mm.svg"
                    os.system(f"python3 tag_to_svg.py {os.path.join(os.fsdecode(directory), filename)}"
                              f" {os.path.join(os.getcwd(),output_folder, output_filename)} --size=140mm")
                else:  # make small tag
                    output_filename = f"{filename_without_ending}_28mm.svg"
                    os.system(f"python3 tag_to_svg.py {os.path.join(os.fsdecode(directory), filename)} "
                              f"{os.path.join(os.getcwd(),output_folder, output_filename)} --size=28mm")


if __name__ == '__main__':
    main()