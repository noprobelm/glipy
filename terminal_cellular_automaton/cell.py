from typing import Protocol

from .coordinate import Coordinate, MooreNeighborhood
from .states import CellState


class Cell(Protocol):
    """Protocol definition for a cell.

    A cell must have:
        1. coord (Coordinate)
        2. state (CellState): This defines a cell's behavior when changing states
        3. neighbors (list[Coordinate]): A list of all valid neighbors for a cell
    """

    coord: Coordinate
    state: CellState
    neighbors: list[Coordinate]


class MooreCell:
    """A cell that references members of a MooreNeighborhood

    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | C | 5 |
    +---+---+---+
    | 6 | 7 | 8 |
    +---+---+---+

    Attributes:
        coord (Coordinate): The coordinate of the cell
        state (CellState): The corresponding CellState
        neighbors (list[Coordinate]): A list of the valid cell neighbors to pass to CellState.change_state
        neighborhood (MooreNeighborhood): The neighborhood to reference when setting neighbors
    """

    neighborhood = MooreNeighborhood

    def __init__(self, coordinate: Coordinate, max_coord: Coordinate, state: CellState):
        """Initializes an instance of the MooreCell class

        Args:
        coord (Coordinate): The coordinate of the cell
        state (CellState): The corresponding CellState
        max_coord (Coordinate): The maximum coordinate in the corresponding matrix (used to cache neighbors)

        """
        self.coord = coordinate
        self.state = state
        self.neighbors = []
        for nc in self.neighborhood:
            c = self.coord + nc.value
            if c in max_coord:
                self.neighbors.append(c)
