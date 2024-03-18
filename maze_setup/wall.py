from dataclasses import dataclass
from enum import Enum
from typing import List
from typing import Optional
import copy as cp


@dataclass
class Size:
    x: int = 0
    y: int = 0


@dataclass
class Position:
    x: int = 0
    y: int = 0
    z: int = 0


class Placement(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Orientation(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


class Tag(object):
    """Describes a AprilTag where orientation means the direction where the AprilTag's z axis points to (Note that the
    AprilTags z-axis always points out of the tag, the tag's x axis to the right (looking at the tag) and the tag's y
    axis to the air (looking at the tag)). Position is the center's position of the tag."""

    def __init__(self, orientation: Optional[Orientation] = None, pos_x: Optional[int] = None,
                 pos_y: Optional[int] = None,
                 pos_z: Optional[int] = None, size_x: Optional[int] = None, size_y: Optional[int] = None,
                 tag_id: int = -1):
        self.tag_id = tag_id
        if None not in [pos_x, pos_y, pos_z]:
            self.position: Position = Position(pos_x, pos_y, pos_z)
        self.orientation: Orientation = orientation
        if None not in [size_x, size_y]:
            self.size: Size = Size(size_x, size_y)


class Wall(object):
    """Describes a wall object where placement means the direction where the smallest tag id heads to, the position in x,
    y, and z is the position of the center of the tag with the smallest id."""

    def __init__(self, placement: Optional[Placement] = None, pos_x: Optional[int] = None, pos_y: Optional[int] = None,
                 pos_z: Optional[int] = None, smallest_tag_id: Optional[int] = None):
        self.width: int = 250  # mm
        self.height: int = 170  # mm
        self.thickness: int = 3  # mm
        self.big_tag_size: int = 140  # mm
        self.small_tag_size: int = 28  # mm
        self.placement: Optional[Placement] = placement
        self.tags: List[Tag] = []
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.smallest_tag_id = smallest_tag_id
        if smallest_tag_id is not None:
            tag_ids = self.get_tag_ids_to_smallest_tag_id(abs(smallest_tag_id))
            if smallest_tag_id < 0:
                # south or east orientation of smallest tag, therefore the order in tag_ids is changed
                new_tag_ids = [tag_ids[2], tag_ids[3], tag_ids[0], tag_ids[1]]
                tag_ids = cp.deepcopy(new_tag_ids)

            for idx, tag_id in enumerate(tag_ids):
                if tag_id is None:
                    continue
                if idx == 0 or idx == 1:  # first two tags look to left or up
                    if self.placement == placement.HORIZONTAL:
                        self.tags.append(Tag(orientation=Orientation.NORTH,
                                             pos_x=pos_x,
                                             pos_y=pos_y,
                                             pos_z=pos_z,
                                             size_x=self.big_tag_size if idx == 0 else self.small_tag_size,
                                             size_y=self.big_tag_size if idx == 0 else self.small_tag_size,
                                             tag_id=tag_id))
                    elif self.placement == placement.VERTICAL:
                        self.tags.append(Tag(orientation=Orientation.WEST,
                                             pos_x=pos_x,
                                             pos_y=pos_y,
                                             pos_z=pos_z,
                                             size_x=self.big_tag_size if idx == 0 else self.small_tag_size,
                                             size_y=self.big_tag_size if idx == 0 else self.small_tag_size,
                                             tag_id=tag_id))
                elif idx == 2 or idx == 3:  # third and forth tag on the other side of the wall
                    if self.placement == placement.HORIZONTAL:
                        self.tags.append(Tag(orientation=Orientation.SOUTH,
                                             pos_x=pos_x + self.thickness,
                                             pos_y=pos_y,
                                             pos_z=pos_z,
                                             size_x=self.big_tag_size if idx == 2 else self.small_tag_size,
                                             size_y=self.big_tag_size if idx == 2 else self.small_tag_size,
                                             tag_id=tag_id))
                    elif self.placement == placement.VERTICAL:
                        self.tags.append(Tag(orientation=Orientation.EAST,
                                             pos_x=pos_x,
                                             pos_y=pos_y + self.thickness,
                                             pos_z=pos_z,
                                             size_x=self.big_tag_size if idx == 2 else self.small_tag_size,
                                             size_y=self.big_tag_size if idx == 2 else self.small_tag_size,
                                             tag_id=tag_id))

    def get_tag_ids_to_smallest_tag_id(self, smallest_id: int):
        """Returns the remaining Tag IDs (including the one given) on one wall.
        The first entry in the dictionary entry is assumed to be the smallest ID on the wall, the second entry is the ID
        of the tag on the same side (front), the third entry is the big tag on the back and the fourth tag is the small
        tag on the back. If there is no tag on the back, the respective entry is None."""
        smallest_id_to_all_ids_on_wall = {
            30: [30, 31, 40, 41],
            24: [24, 25, 46, 47],
            8: [8, 9, 14, 15],
            28: [28, 29, 42, 43],
            34: [34, 35, 36, 37],
            4: [4, 5, 18, 19],
            6: [6, 7, 16, 17],
            26: [26, 27, 44, 45],
            10: [10, 11, 12, 13],
            2: [2, 3, 20, 21],
            32: [32, 33, 38, 39],
            0: [0, 1, 22, 23],
            48: [48, 49, None, None],
            52: [52, 53, None, None],
            56: [56, 57, None, None],
            60: [60, 61, None, None],
            64: [64, 65, None, None],
            68: [68, 69, None, None],
            72: [72, 73, None, None],
            76: [76, 77, None, None],
            80: [80, 81, None, None],
            84: [84, 85, None, None],
            88: [88, 89, None, None],
            92: [92, 93, None, None],
            96: [96, 97, 98, 99],
            100: [100, 101, 102, 103],
            104: [104, 105, 106, 107],
            108: [108, 109, 110, 111],
            112: [112, 113, 114, 115],
            116: [116, 117, 118, 119],
            120: [120, 121, 122, 123],
            124: [124, 125, 126, 127],
            128: [128, 129, 130, 131],
            132: [132, 133, 134, 135],
            136: [136, 137, 138, 139],
            140: [140, 141, 142, 143],
            144: [144, 145, 146, 147],
            148: [148, 149, 150, 151],
            152: [152, 153, 154, 155],
            156: [156, 157, 158, 159],
            160: [160, 161, 162, 163],
            164: [164, 165, 166, 167],
            168: [168, 169, 170, 171],
            172: [172, 173, 174, 175],
            176: [176, 177, 178, 179],
            180: [180, 181, 182, 183],
            184: [184, 185, 186, 187],
            188: [188, 189, 190, 191],
            192: [192, 193, None, None],
            196: [196, 197, None, None],
            200: [200, 201, None, None],
            204: [204, 205, None, None],
            208: [208, 209, None, None],
            212: [212, 213, None, None],
            216: [216, 217, None, None],
            220: [220, 221, None, None],
            224: [224, 225, None, None],
            228: [228, 229, None, None],
            232: [232, 233, None, None],
            236: [236, 237, None, None],
            240: [240, 241, None, None],
            244: [244, 245, None, None],
            248: [248, 249, None, None],
            252: [252, 253, None, None],
            256: [256, 257, None, None],
            260: [260, 261, None, None],
            264: [264, 265, None, None],
            268: [268, 269, None, None],
            272: [272, 273, None, None],
            276: [276, 277, None, None],
            280: [280, 281, None, None],
            284: [284, 285, None, None],
            288: [288, 289, None, None],
            292: [292, 293, None, None],
            296: [296, 297, None, None],
            300: [300, 301, None, None],
            304: [304, 305, None, None],
            308: [308, 309, None, None],
            312: [312, 313, None, None],
            316: [316, 317, None, None],
            320: [320, 321, None, None],
            324: [324, 325, None, None],
            328: [328, 329, None, None],
            332: [332, 333, None, None]
        }
        for key, val in smallest_id_to_all_ids_on_wall.items():
            assert key == val[0], "First entry in the dictionary values must be the key"
            assert len(val) == 4, "Length of dict entry must be 4."
            for v in val[1:]:
                if v is not None:
                    assert v > val[0], "Smallest ID must be first entry in dictionary values"

        if smallest_id not in smallest_id_to_all_ids_on_wall.keys():
            print(
                "There is said to be an ID {smallest_id} that does not exist in the database. Either its not defined there,"
                "or the given ID is wrong.")
            assert 1 == 0
        return smallest_id_to_all_ids_on_wall[smallest_id]
