"""The coordinate system used by the Matrix2D class"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class Coordinate:
    """An x/y coordinate to reference location in a Matrix2D"""

    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        """Returns the sum of one coordinate and another. Primarily used to identify neighbors"""
        return Coordinate(self.x + other.x, self.y + other.y)

    def __contains__(self, other: Coordinate) -> bool:
        if 0 <= other.x <= self.x and 0 <= other.y <= self.y:
            return True
        return False
