#!/usr/bin/env python3

"""Defines the Matrix2D class"""

from __future__ import annotations

from copy import copy
from typing import Any, List

from .coordinate import Coordinate


class Matrix2D:
    """Generic contiguous 2d matrix capable of storing any type.

    The matrix is filled with "None" by default. It is up to the user to fill out the matrix with compatible objects.

    Attributes:
        max_coord (Coordinate): The maximum valid coordinate found in the grid
        matrix (List): The underlying 2d matrix

    """

    def __init__(self, xmax: int, ymax: int) -> None:
        """Initializes a Matrix2D instance

        Generates a new grid filled with type 'NoneType'

        Args:
            xmax (int): The maximum x value in the grid
            ymax (int): The maximum y value in the grid

        """
        self.max_coord = Coordinate(xmax - 1, ymax - 1)
        self.matrix: List[List[Any]] = []
        for y in range(ymax):
            self.matrix.append([])
            for _ in range(xmax):
                self.matrix[y].append(None)

    def __contains__(self, coord: Coordinate):
        """Checks if a given coordinate is within range of the matrix

        Args:
            coord (Coordinate): The coordinate to check against
        """

        if 0 <= coord.x <= self.max_coord.x and 0 <= coord.y <= self.max_coord.y:
            return True
        return False

    def __getitem__(self, coord: Coordinate):
        """Gets a cell from a provided coordinate

        Args:
            coord (Coordinate): The coordinate of the cell to get
        """
        return self.matrix[coord.y][coord.x]

    def __setitem__(self, coord: Coordinate, item: Any):
        """Sets a given coordinate to an item

        Args:
            coord (Coordinate): The coordinate of the cell to get
        """

        self.matrix[coord.y][coord.x] = item

    def __copy__(self) -> Matrix2D:
        matrix = Matrix2D(self.max_coord.x + 1, self.max_coord.y + 1)
        for y in range(self.max_coord.y + 1):
            for x in range(self.max_coord.x + 1):
                matrix[Coordinate(x, y)] = copy(self[Coordinate(x, y)])
        return matrix
