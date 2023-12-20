from .matrix import CellMatrix
from .moore_cell import MooreCell


class ConwayState:
    def __init__(self, alive: bool):
        self.alive = alive

    def change_state(self, neighbors: list[MooreCell], matrix: CellMatrix):
        alive_count = 0
        for nc in neighbors:
            n = matrix[nc]
            if n.alive is True:
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
