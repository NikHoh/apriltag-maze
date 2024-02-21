#!/usr/bin/env python3
import os.path
import copy as cp
import numpy as np

def read_svg_tag(tag_number:int):
    """Read tag svg and strip to relevant data"""
    if tag_number % 2 == 0:
        tag_file_name = f"tag48_12_{str(tag_number).zfill(5)}_140mm.svg"
    else:
        tag_file_name = f"tag48_12_{str(tag_number).zfill(5)}_28mm.svg"

    path_to_tag = os.path.join(os.getcwd(), "tags_scaled", tag_file_name)

    tag_string = read_svg_file(path_to_tag)

    tag_string = tag_string.split('xmlns="http://www.w3.org/2000/svg">')[1]
    tag_string = tag_string.split("</svg>")[0]

    return tag_string



def read_svg_file(path:str) -> str:
    """Reads in text from a path"""
    assert os.path.isfile(path), f"Given path {path} does not exist"
    with open(path) as f:
        s = f.read()
    return s

def save_svg_file(string_to_save:str, path:str):
    """Writes text to a path"""
    assert not os.path.isfile(path), "Filename that you want to use to save already exits. Choose another one."
    with open(path, 'w') as f:
        f.write(string_to_save)

def replace_string_in_string(complete_string:str, old_string:str, new_string:str) -> str:
    """Replaces a text within a string"""
    assert old_string in complete_string, f"Expected string {old_string} not found in complete string"
    return complete_string.replace(old_string, new_string)



def main():
    """Takes an info if the front or the back of a lasered MDF plate (1100mm x 550mm) should be created (bool)
     and a list of 12 even integers that are the respective AprilTag ids that are supposed to be on the plate.
     There is some convention in the order of tags for front and back (see examples). They are assigned in such an order
     so that a single wall has for example the tags 0 (big) and 1 (small) on the front and the following tag ids
     2 (big) and 3 (small) on the back.
     There are 2 x 6 walls (170mm x 250mm) (portrait orientation) on a plate (landscape orientation). They are
     indexed beginning on the top left of the plate going to the right, and then down."""

    # USER INPUT START
    name_for_new_svg_file = "Plate_4_hinten.svg"

    # Do you want to create front (with laser cut) or back?
    front = False

    # A plate consists of 12 walls (25cm x 17cm) that are arranged 2 x 6 on the plate.
    # Give the Tag numbers that you want to have on the wall (only even ones are accepted as every even tag is
    # accompanied by a small uneven (+1) one that is placed within the big one). Tags are ordered beginning from left to
    # right, then top to bottom

    # tag_numbers = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44] # Plate 1 front (double plate)
    # tag_numbers = [22, 18, 14, 10, 6, 2, 46, 42, 38, 34, 30, 26] # Plate 1 back

    # tag_numbers = [48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92] # Plate 2 front (single plate)
    # tag_numbers = [70, 66, 62, 58, 54, 50, 94, 90, 86, 82, 78, 74] # reserved for Plate 2 back (will never be used)

    # tag_numbers = [96, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140]  # Plate 3 front (double plate)
    # tag_numbers = [118, 114, 110, 106, 102,  98, 142, 138, 134, 130, 126, 122] # Plate 3 back

    # tag_numbers = [144, 148, 152, 156, 160, 164, 168, 172, 176, 180, 184, 188]  # Plate 4 front (double plate)
    tag_numbers = [166, 162, 158, 154, 150, 146, 190, 186, 182, 178, 174, 170] # Plate 4 back

    # tag_numbers = [192, 196, 200, 204, 208, 212, 216, 220, 224, 228, 232, 236] # Plate 5 front (single plate)
    # tag_numbers = [214, 210, 206, 202, 198, 194, 238, 234, 230, 226, 222, 218] # reserved for Plate 5 back (will never be used)

    # tag_numbers = [240, 244, 248, 252, 256, 260, 264, 268, 272, 276, 280, 284] # Plate 6 front (single plate)
    # tag_numbers = [262, 258, 254, 250, 246, 242, 286, 282, 278, 274, 270, 266] # reserved for Plate 6 back (will never be used)

    # tag_numbers = [288, 292, 296, 300, 304, 308, 312, 316, 320, 324, 328, 332] # Plate 7 front (single plate)
    # tag_numbers = [310, 306, 302, 298, 294, 290, 334, 330, 326, 322, 318, 314] # reserved for Plate 7 back (will never be used)


    # USER INPUT END

    path_to_new_svg_file = os.path.join(os.getcwd(), "final_plates_to_laser", name_for_new_svg_file)

    # Do not change anything from here on
    assert len(tag_numbers) == 12, "There must be given 12 tag numbers"
    for idx, tag_number in enumerate(tag_numbers):
        assert tag_number%2 == 0, "Tag numbers must be even"
        if idx == 0:
            continue
        if front:
            assert tag_number == tag_numbers[idx-1]+4, "Front plate tag numbers should always be spaced 4"
        else:
            assert int(np.abs(tag_number - tag_numbers[idx-1])) in [4, 44], "Back plate numbers no not follow specified convention. See given expamples"



    assert not os.path.isfile(path_to_new_svg_file), "New svg file that is supposed to be created does alreaddy exist, choose other name"

    # complete the tag_numbers with the respective uneven ones
    new_tag_numbers = []
    for tag_number in tag_numbers:
        new_tag_numbers.append(tag_number)
        new_tag_numbers.append(tag_number+1)
    tag_numbers = cp.deepcopy(new_tag_numbers)
    del new_tag_numbers

    if front:
        path_to_svg = os.path.join(os.getcwd(), "do_not_touch", "sample_vorne_empty.svg")
        # left to right, top to bottom
        blueprints_for_tags = ["hier_tag_000",
                               "hier_tag_001",
                               "hier_tag_004",
                               "hier_tag_005",
                               "hier_tag_008",
                               "hier_tag_009",
                               "hier_tag_012",
                               "hier_tag_013",
                               "hier_tag_016",
                               "hier_tag_017",
                               "hier_tag_020",
                               "hier_tag_021",
                               "hier_tag_024",
                               "hier_tag_025",
                               "hier_tag_028",
                               "hier_tag_029",
                               "hier_tag_032",
                               "hier_tag_033",
                               "hier_tag_036",
                               "hier_tag_037",
                               "hier_tag_040",
                               "hier_tag_041",
                               "hier_tag_044",
                               "hier_tag_045"]
        blueprints_for_texts = ["id000 &amp; id001",
                                "id004 &amp; id005",
                                "id008 &amp; id009",
                                "id012 &amp; id013",
                                "id016 &amp; id017",
                                "id020 &amp; id021",
                                "id024 &amp; id025",
                                "id028 &amp; id029",
                                "id032 &amp; id033",
                                "id036 &amp; id037",
                                "id040 &amp; id041",
                                "id044 &amp; id045"]
    else:
        path_to_svg = os.path.join(os.getcwd(), "do_not_touch", "sample_hinten_empty.svg")
        blueprints_for_tags = ["hier_tag_022",
                               "hier_tag_023",
                               "hier_tag_018",
                               "hier_tag_019",
                               "hier_tag_014",
                               "hier_tag_015",
                               "hier_tag_010",
                               "hier_tag_011",
                               "hier_tag_006",
                               "hier_tag_007",
                               "hier_tag_002",
                               "hier_tag_003",
                               "hier_tag_046",
                               "hier_tag_047",
                               "hier_tag_042",
                               "hier_tag_043",
                               "hier_tag_038",
                               "hier_tag_039",
                               "hier_tag_034",
                               "hier_tag_035",
                               "hier_tag_030",
                               "hier_tag_031",
                               "hier_tag_026",
                               "hier_tag_027"]
        blueprints_for_texts = ["id022 &amp; id023",
                                "id018 &amp; id019",
                                "id014 &amp; id015",
                                "id010 &amp; id011",
                                "id006 &amp; id007",
                                "id002 &amp; id003",
                                "id046 &amp; id047",
                                "id042 &amp; id043",
                                "id038 &amp; id039",
                                "id034 &amp; id035",
                                "id030 &amp; id031",
                                "id026 &amp; id027"]

    svg_file = read_svg_file(path_to_svg)


    for idx, tag_number in enumerate(tag_numbers):
        # replace tags
        svg_tag = read_svg_tag(tag_number)
        old_tag_string = blueprints_for_tags[idx]
        svg_file = replace_string_in_string(svg_file, old_tag_string, svg_tag)

        # replace text (only once per wall so only when even)
        if idx % 2 == 0:
            new_text = f"id{str(tag_number).zfill(3)} &amp; id{str(tag_number+1).zfill(3)}"
            old_text = blueprints_for_texts[int(idx/2)]
            svg_file = replace_string_in_string(svg_file, old_text, new_text)


    save_svg_file(svg_file, path_to_new_svg_file)







if __name__ == '__main__':
    main()