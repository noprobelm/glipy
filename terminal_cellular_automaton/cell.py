from typing import Protocol, Tuple

from .coordinate import Coordinate


class Cell(Protocol):
    neighbors: tuple[Coordinate, ...]
    coord: Coordinate

    def __init__(self, coord: Coordinate) -> None:
        ...

    def get_neighbors(self, max_coord: Coordinate) -> list[Coordinate]:
        ...


class MooreCell:
    """A cell that references members of a MooreNeighborhood

    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | C | 5 |
    +---+---+---+
    | 6 | 7 | 8 |
    +---+---+---+

    """

    neighbors: Tuple[Coordinate, ...] = (
        # Upper left
        Coordinate(-1, -1),
        # Upper
        Coordinate(0, -1),
        # Upper right
        Coordinate(1, -1),
        # Right
        Coordinate(1, 0),
        # Lower right
        Coordinate(1, 1),
        # Lower
        Coordinate(0, 1),
        # Lower left
        Coordinate(-1, 1),
        # Left
        Coordinate(-1, 0),
    )

    def __init__(self, coord: Coordinate):
        self.coord = coord

    def get_neighbors(self, max_coord: Coordinate) -> list[Coordinate]:
        neighbors = []
        for nc in self.neighbors:
            n = nc + self.coord
            if n in max_coord:
                neighbors.append(n)

        return neighbors
