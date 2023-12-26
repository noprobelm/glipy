"""Use this module to create commonly accessed patterns"""
from .state import ConwayState
from .coordinate import Coordinate
from .matrix import Matrix2D


class Glider(Matrix2D):
    def __init__(self):
        super().__init__(3, 3)
        coords = [[2, 0], [0, 1], [2, 1], [1, 2], [2, 2]]
        for y in range(3):
            for x in range(3):
                coord = Coordinate(x, y)
                if [x, y] in coords:
                    self[coord] = ConwayState(alive=True)
                else:
                    self[coord] = ConwayState(alive=False)

        for x, y in coords:
            coord = Coordinate(x, y)
