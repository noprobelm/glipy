from __future__ import annotations

from typing import Protocol

from .coordinate import Coordinate, MooreNeighborhood
from .matrix import Matrix2D
from .states import CellState


class Cell(Protocol):
    coord: Coordinate
    state: CellState
    neighbors: list[Cell]


class MooreCell:
    def __init__(self, coordinate: Coordinate, state: CellState, matrix: Matrix2D):
        self.coord = coordinate
        self.state = state
        self.neighbors = []
        for n in MooreNeighborhood:
            nc = self.coord + n.value
            if nc in matrix:
                self.neighbors.append(nc)
