"""Use this module to create commonly accessed patterns"""
from .state import ConwayState
from .coordinate import Coordinate
from .matrix import Matrix2D


class HorizontalLine(Matrix2D):
    def __init__(self, length: int):
        super().__init__(length, 1)
        for x in range(length):
            self[Coordinate(x, 0)] = ConwayState(True)


class VerticalLine(Matrix2D):
    def __init__(self, length: int):
        super().__init__(1, length)
        for x in range(length):
            self[Coordinate(x, 0)] = ConwayState(True)


class Glider(Matrix2D):
    def __init__(self):
        super().__init__(3, 3)
        coords = [[2, 0], [0, 1], [2, 1], [1, 2], [2, 2]]
        for y in range(3):
            for x in range(3):
                coord = Coordinate(x, y)
                if [x, y] in coords:
                    self[coord] = ConwayState(True)
                else:
                    self[coord] = ConwayState(False)


class Pulsar(Matrix2D):
    def __init__(self):
        super().__init__(13, 13)
        for y in [0, 5, 7, 12]:
            for x in [2, 3, 4, 8, 9, 10]:
                self[Coordinate(x, y)] = ConwayState(True)
        for x in [0, 5, 7, 12]:
            for y in [2, 3, 4, 8, 9, 10]:
                self[Coordinate(x, y)] = ConwayState(True)
