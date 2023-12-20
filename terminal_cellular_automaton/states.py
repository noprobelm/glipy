from typing import Protocol, Tuple

from .coordinate import Coordinate
from .matrix import Matrix2D


class CellState(Protocol):
    colors: Tuple[str, str]

    def change_state(self, neighbors: list[Coordinate], matrix: Matrix2D):
        pass


class ConwayState:
    def __init__(self, colors: Tuple[str, str], alive: bool):
        self.colors = colors
        self.alive = alive

    @property
    def color(self):
        if self.alive is True:
            return self.colors[0]
        return self.colors[1]

    def change_state(self, neighbors: list[Coordinate], matrix: Matrix2D):
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
