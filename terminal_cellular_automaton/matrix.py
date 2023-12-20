#!/usr/bin/env python3

"""Hosts the CellMatrix class used to run the simulation"""

from rich.console import Console, ConsoleOptions, RenderResult
from rich.segment import Segment
from rich.style import Style

from .coordinate import Coordinate
from random import randint
from .cell import MooreCellState


class CellMatrix:
    """This class acts as the directory for all elements in the simulation

    Since the matrix will always be continuous ('Empty' elements represent empty space), we subclass from list to enable
    efficient lookup of elements. A dictionary-like structure would usually be less efficient, especially when updating
    values, due to the necessity of rehashing keys.

    Attributes:
        max_coord (Coordinate): The maximum valid coordinate found in the grid
        midpoint (Coordinate): The midpoint of the grid.

    """

    def __init__(self, xmax: int, ymax: int) -> None:
        """Initializes a CellMatrix instance

        Generates a new grid full of 'Empty' elements

        Args:
            xmax (int): The maximum x value in the grid
            ymax (int): The maximum y value in the grid

        """
        self.max_coord = Coordinate(xmax - 1, ymax - 1)
        self.matrix = []
        for y in range(ymax):
            self.matrix.append([])
            for x in range(xmax):
                self.matrix[y].append(None)

    def __contains__(self, coord: Coordinate):
        if 0 <= coord.x <= self.max_coord.x and 0 <= coord.y <= self.max_coord.y:
            return True
        return False

    def __getitem__(self, coord: Coordinate):
        if isinstance(coord, Coordinate):
            return self.matrix[coord.y][coord.x]
        else:
            raise TypeError("Index must be a Coordinate instance")

    def __setitem__(self, coord: Coordinate, value):
        if isinstance(coord, Coordinate):
            self.matrix[coord.y][coord.x] = value
        else:
            raise TypeError("Index must be a Coordinate instance")

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Renders each Cell in the simulation using the Rich Console Protocol

        Due to the typical 2:1 height/width aspect ratio of a terminal, each cell rendered from the CellMatrix simulation
        actually occupies 2 rows in the terminal. I picked up this trick from rich's __main__ module. Run
        'python -m rich and observe the color palette at the top of stdout for another example of what this refers to.

        Yields:
            2 cells in the simulation, row by row, until all cell states have been rendered.
        """
        for y in range(self.max_coord.y)[::2]:
            for x in range(self.max_coord.x + 1):
                bg = self.matrix[y][x].state.value
                fg = self.matrix[y + 1][x].state.value
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()
