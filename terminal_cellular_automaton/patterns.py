"""Use this module to create commonly accessed patterns"""

from .matrix import Matrix2D
from .state import ConwayState, CellState
from typing import List, Sequence
from . import reader
from .coordinate import Coordinate


def fill_dead(xmax: int, ymax: int, alive: Sequence[Coordinate]):
    states = []
    for y in range(ymax + 1):
        states.append([])
        for x in range(xmax + 1):
            if Coordinate(x, y) in alive:
                states[y].append(ConwayState(True))
            else:
                states[y].append(ConwayState(False))
    return states


class Pattern(Matrix2D):
    def __init__(self, xmax: int, ymax: int, states: List[List[CellState]]):
        super().__init__(xmax, ymax, states)

    @classmethod
    def from_life(cls, path: str):
        data = reader.life(path)
        return cls(*data)

    @classmethod
    def from_rle(cls, path: str):
        data = reader.rle(path)
        return cls(data.xmax, data.ymax, data.states)


class Glider(Pattern):
    def __init__(self):
        xmax = 2
        ymax = 2
        states = []
        alive = (
            Coordinate(0, 2),
            Coordinate(1, 0),
            Coordinate(2, 1),
            Coordinate(1, 2),
            Coordinate(2, 2),
        )

        states = fill_dead(xmax, ymax, alive)
        super().__init__(xmax, ymax, states)


class Pulsar(Pattern):
    def __init__(self):
        xmax = 12
        ymax = 12
        states = []
        alive = [
            Coordinate(x, y)
            for x, y in (
                (2, 0),
                (3, 0),
                (4, 0),
                (8, 0),
                (9, 0),
                (10, 0),
                (2, 5),
                (3, 5),
                (4, 5),
                (8, 5),
                (9, 5),
                (10, 5),
                (2, 7),
                (3, 7),
                (4, 7),
                (8, 7),
                (9, 7),
                (10, 7),
                (2, 12),
                (3, 12),
                (4, 12),
                (8, 12),
                (9, 12),
                (10, 12),
                (0, 2),
                (0, 3),
                (0, 4),
                (0, 8),
                (0, 9),
                (0, 10),
                (5, 2),
                (5, 3),
                (5, 4),
                (5, 8),
                (5, 9),
                (5, 10),
                (7, 2),
                (7, 3),
                (7, 4),
                (7, 8),
                (7, 9),
                (7, 10),
                (12, 2),
                (12, 3),
                (12, 4),
                (12, 8),
                (12, 9),
                (12, 10),
            )
        ]
        states = fill_dead(xmax, ymax, alive)

        super().__init__(xmax, ymax, states)


class CloverLeaf(Pattern):
    def __init__(self):
        xmax = 8
        ymax = 10
        states = []
        alive = [
            Coordinate(x, y)
            for x, y in (
                (3, 0),
                (5, 0),
                (1, 1),
                (2, 1),
                (3, 1),
                (5, 1),
                (6, 1),
                (7, 1),
                (0, 2),
                (4, 2),
                (8, 2),
                (0, 3),
                (2, 3),
                (6, 3),
                (8, 3),
                (1, 4),
                (2, 4),
                (4, 4),
                (6, 4),
                (7, 4),
                (1, 6),
                (2, 6),
                (4, 6),
                (6, 6),
                (7, 6),
                (0, 7),
                (2, 7),
                (6, 7),
                (8, 7),
                (0, 8),
                (4, 8),
                (8, 8),
                (1, 9),
                (2, 9),
                (3, 9),
                (5, 9),
                (6, 9),
                (7, 9),
                (3, 10),
                (5, 10),
            )
        ]

        states = fill_dead(xmax, ymax, alive)

        super().__init__(xmax, ymax, states)
