from typing import Protocol

from .coordinate import Coordinate
from .matrix import CellMatrix


class CellState(Protocol):
    color: str

    def change_state(self, matrix: CellMatrix):
        pass


class ConwayState:
    def __init__(self, alive: bool):
        self.alive = alive

    @property
    def color(self):
        if self.alive == True:
            return "green"
        return "red"

    def change_state(self, neighbors: list[Coordinate], matrix: CellMatrix):
        alive_count = 0
        for nc in neighbors:
            n = matrix[nc]
            if n.state.alive is True:
                alive_count += 1

        match self.alive:
            case True:
                if alive_count == 2 or alive_count == 3:
                    return
                else:
                    self.alive = False

            case False:
                if alive_count == 3:
                    self.alive = True
