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
        coords = [
            [2, 0],
            [3, 0],
            [4, 0],
            [8, 0],
            [9, 0],
            [10, 0],
            [2, 5],
            [3, 5],
            [4, 5],
            [8, 5],
            [9, 5],
            [10, 5],
            [2, 7],
            [3, 7],
            [4, 7],
            [8, 7],
            [9, 7],
            [10, 7],
            [2, 12],
            [3, 12],
            [4, 12],
            [8, 12],
            [9, 12],
            [10, 12],
            [0, 2],
            [0, 3],
            [0, 4],
            [0, 8],
            [0, 9],
            [0, 10],
            [5, 2],
            [5, 3],
            [5, 4],
            [5, 8],
            [5, 9],
            [5, 10],
            [7, 2],
            [7, 3],
            [7, 4],
            [7, 8],
            [7, 9],
            [7, 10],
            [12, 2],
            [12, 3],
            [12, 4],
            [12, 8],
            [12, 9],
            [12, 10],
        ]
        for x in range(13):
            for y in range(13):
                if [x, y] in coords:
                    self[Coordinate(x, y)] = ConwayState(True)
                else:
                    self[Coordinate(x, y)] = ConwayState(False)
