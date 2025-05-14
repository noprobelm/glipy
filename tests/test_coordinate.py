"""Tests Coordinate behavior"""

from ward import test

from glipy.coordinate import Coordinate


@test(
    "Adding 2 coordinates will result in a new coordinate whose x/y values are the sum of the others",
)
def _():
    assert Coordinate(1, 1) + Coordinate(1, 1) == Coordinate(2, 2)


@test(
    "Subtracting 2 coordinates will result in a new coordinate whose x/y values are the difference of the others",
)
def _():
    assert Coordinate(1, 1) - Coordinate(1, 1) == Coordinate(0, 0)


@test(
    "A coordinate is within another coordinate if its x and y values are greater than 0 and less than the coordinte \
being compared against",
)
def _():
    assert Coordinate(0, 0) in Coordinate(1, 1)
    assert Coordinate(2, 2) not in Coordinate(1, 1)
    assert Coordinate(-1, -1) not in Coordinate(1, 1)
