from enum import Enum
from typing import Optional
from dataclasses import dataclass
from typing import List

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
    def __init__(self, orientation: Optional[Orientation] = None, pos_x: Optional[int] = None, pos_y: Optional[int] = None,
                 pos_z: Optional[int] = None, size_x: Optional[int] = None, size_y: Optional[int] = None, tag_id:int =-1):
        self.tag_id = tag_id
        if None not in [pos_x, pos_y, pos_z]:
            self.position: Position = Position(pos_x, pos_y, pos_z)
        self.orientation: Orientation = orientation
        if None not in [size_x, size_y]:
            self.size: Size = Size(size_x, size_y)


class Wall(object):
    """Describes a wall object where placement means the direction where the smallest tag id heads to, the position in x,
    y, and z is the position of the center of the tag with the smallest id."""
    def __init__(self, placement:Optional[Placement] = None, pos_x: Optional[int] = None, pos_y: Optional[int] = None,
                 pos_z: Optional[int] = None, smallest_tag_id: Optional[int] = None):
        self.width: int = 250 # mm
        self.height: int = 170 # mm
        self.thickness: int = 3 # mm
        self.big_tag_size: int = 140 # mm
        self.small_tag_size: int = 28 # mm
        self.placement: Optional[Placement] = placement
        self.tags: List[Tag] = []
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        if smallest_tag_id is not None:
            tag_ids = list(range(smallest_tag_id, smallest_tag_id+4))
            for idx, tag_id in enumerate(tag_ids):
                if idx == 0 or idx == 1: # first two tags look to left or up
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
                elif idx == 2 or idx == 3: # third and forth tag on the other side of the wall
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