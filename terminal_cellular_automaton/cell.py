from __future__ import annotations
from enum import Enum
from .coordinate import Coordinate, MooreNeighborhood


class MooreCellState(Enum):
    ON = "GREEN"
    OFF = "RED"


class MooreCell:
    def __init__(self, coordinate: Coordinate, state: MooreCellState, matrix):
        self.coord = coordinate
        self.state = state
        self.neighbors = []
        for n in MooreNeighborhood:
            nc = self.coord + n.value
            if nc in matrix:
                self.neighbors.append(nc)

    def change_state(self, matrix):
        on = 0
        match self.state:
            case MooreCellState.OFF:
                for nc in self.neighbors:
                    n = matrix[nc]
                    if n.state == MooreCellState.ON:
                        on += 1
                if on == 3:
                    self.state = MooreCellState.ON
                    return

            case MooreCellState.ON:
                for nc in self.neighbors:
                    n = matrix[nc]
                    if n.state == MooreCellState.ON:
                        on += 1
                if on == 2 or on == 3:
                    return

                self.state = MooreCellState.OFF
