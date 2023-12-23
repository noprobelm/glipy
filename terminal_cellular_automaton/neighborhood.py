from .coordinate import Coordinate
from enum import Enum


class MooreNeighborhood(Enum):
    """Enumeration for variants of neighbors found in a Moore Neighborhood"""

    UPPER_LEFT = Coordinate(-1, -1)
    UPPER = Coordinate(0, -1)
    UPPER_RIGHT = Coordinate(1, -1)
    RIGHT = Coordinate(1, 0)
    LOWER_RIGHT = Coordinate(1, 1)
    LOWER = Coordinate(0, 1)
    LOWER_LEFT = Coordinate(-1, 1)
    LEFT = Coordinate(-1, 0)
