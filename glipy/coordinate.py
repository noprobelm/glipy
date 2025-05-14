"""The coordinate system used by the Automaton class."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Coordinate:
    """An x/y coordinate to reference location in a 2 dimensional matrix."""

    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        """Return the sum of one coordinate and another. Primarily used to identify neighbors."""
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Coordinate) -> Coordinate:
        """Return the sum of one coordinate and another. Primarily used to identify neighbors."""
        return Coordinate(self.x - other.x, self.y - other.y)

    def __contains__(self, other: Coordinate) -> bool:
        """Return whether this coordinate is greater than another coordinate."""
        return bool(0 <= other.x <= self.x and 0 <= other.y <= self.y)
