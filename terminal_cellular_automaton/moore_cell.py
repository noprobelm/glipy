from __future__ import annotations

from .coordinate import Coordinate, MooreNeighborhood
from .matrix import CellMatrix


class MooreCell:
    def __init__(self, coordinate: Coordinate, state: MooreCellState, matrix):
        self.coord = coordinate
        self.neighbors = []
        for n in MooreNeighborhood:
            nc = self.coord + n.value
            if nc in matrix:
                self.neighbors.append(nc)
