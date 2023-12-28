"""Defines the Matrix2D class"""

from __future__ import annotations

from copy import copy
from typing import Any, List, Optional, Union

from .coordinate import Coordinate


class Matrix2D:
    """Generic contiguous 2d matrix capable of storing any type.

    The matrix is filled with "None" by default. It is up to the user to fill out the matrix with compatible objects.

    Attributes:
        xmax (int): The maximum x coordinate
        ymax (int): The maximum y coordinate
        max_coord (Coordinate): The maximum valid coordinate found in the grid
        midpoint (Coordinate): The midpoint of the matrix
        matrix (List[List[Any]]): The underlying 2d matrix

    """

    def __init__(
        self,
        xmax: int,
        ymax: int,
        fill_with: Optional[Union[Any, List[List[Any]]]] = None,
    ) -> None:
        """Initializes a Matrix2D instance

        Generates a new grid filled with specified type

        Args:
            xmax (int): The maximum x value in the grid
            ymax (int): The maximum y value in the grid

        """
        self.xmax = xmax
        self.ymax = ymax
        self.max_coord = Coordinate(self.xmax, self.ymax)
        self.midpoint = Coordinate(self.xmax // 2, self.ymax // 2)
        if isinstance(fill_with, list):
            matrix = fill_with
        else:
            matrix = []
            for y in range(self.ymax + 1):
                matrix.append([])
                for _ in range(self.xmax + 1):
                    matrix[y].append(fill_with)

        self.matrix = matrix

    def __contains__(self, coord: Coordinate):
        """Checks if a given coordinate is within range of the matrix

        Args:
            coord (Coordinate): The coordinate to check against
        """

        return coord in self.max_coord

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
        """Returns a shallow copy of an instance

        Returns:
            A shallow copy of a Matrix2D instance
        """
        matrix = Matrix2D(self.xmax, self.ymax)
        for y in range(self.ymax + 1):
            for x in range(self.xmax + 1):
                matrix[Coordinate(x, y)] = copy(self[Coordinate(x, y)])
        return matrix
