from typing import Protocol

from .coordinate import Coordinate, MooreNeighborhood
from .matrix import Matrix2D
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
    """

    def __init__(self, coordinate: Coordinate, state: CellState, matrix: Matrix2D):
        """Initializes an instance of the MooreCell class

        Args:
        coord (Coordinate): The coordinate of the cell
        state (CellState): The corresponding CellState
        matrix (Matrix2D): Reference to the underlying matrix. Used to set neighbors

        """
        self.coord = coordinate
        self.state = state
        self.neighbors = []
        for n in MooreNeighborhood:
            nc = self.coord + n.value
            if nc in matrix:
                self.neighbors.append(nc)
