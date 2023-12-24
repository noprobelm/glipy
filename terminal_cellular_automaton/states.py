from __future__ import annotations

from typing import List, Self, Tuple, Protocol
from .coordinate import Coordinate


class CellState(Protocol):
    @property
    def color(self) -> str:
        ...

    def change_state(self, neighbors: list[Self]) -> CellState:
        ...


class ConwayState:
    """A ConwayState

    This will emulate the classic rules to "Conway's Game of Life"

    - If a cell is ALIVE and is adjacent to 2 or 3 other cells that are also ALIVE, the cell will become DEAD
    - If a cell is DEAD and is adjacent to exactly 3 other cells that are ALIVE, the cell will become ALIVE

    Attributes:
        colors (Tuple[str, str]): A tuple of colors (see Textualize's documentation for 'rich' for accepted values).
                                      The first index is the color for ALIVE states. 2nd is DEAD
        alive (bool): Flag for whether the cell is ALIVE (True) or DEAD (False)
    """

    _colors = ("green", "red")

    def __init__(self, alive: bool = False):
        """Initializes an instance of the ConwayState class

        Args
            colors (Tuple[str, str]): A tuple of colors (see Textualize's documentation for 'rich' for accepted values).
                                      The first index is the color for ALIVE states. 2nd is DEAD
            alive (bool): Flag for whether the cell is ALIVE (True) or DEAD (False)
        """
        self.alive = alive

    @property
    def color(self) -> str:
        if self.alive is True:
            return self.colors[0]
        return self.colors[1]

    @property
    def colors(self):
        return ConwayState._colors

    @colors.setter
    def colors(self, colors: Tuple[str, str]) -> None:
        ConwayState._colors = colors

    def change_state(self, neighbors: List[ConwayState]) -> ConwayState:
        """Changes the state of the cell

        - If a cell is ALIVE and is adjacent to 2 or 3 other cells that are also ALIVE, the cell will become DEAD
        - If a cell is DEAD and is adjacent to exactly 3 other cells that are ALIVE, the cell will become ALIVE

        Args:
            neighbors (List[ConwayState]): A list of neighbor's states
        """
        alive_count = 0
        for n in neighbors:
            if n.alive is True:
                alive_count += 1

        match self.alive:
            case True:
                if alive_count == 2 or alive_count == 3:
                    return ConwayState(True)
                else:
                    return ConwayState(False)

            case False:
                if alive_count == 3:
                    return ConwayState(True)
                else:
                    return ConwayState(False)
