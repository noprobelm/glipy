"""Tests the get_neighbors method for all Cell types."""

from ward import fixture, test

from glipy.cell import MooreCell, NeumannCell
from glipy.coordinate import Coordinate


@fixture
def max_coord() -> Coordinate:
    """Return the maximum coordinate for this test set."""
    return Coordinate(2, 2)


@test("A centrally located MooreCell will have 8 neighbors in its immediate area")
def _() -> None:
    c = MooreCell(Coordinate(1, 1))
    neighbors = c.get_neighbors(max_coord())
    for n in [
        Coordinate(0, 0),
        Coordinate(1, 0),
        Coordinate(2, 0),
        Coordinate(0, 1),
        Coordinate(2, 1),
        Coordinate(0, 2),
        Coordinate(1, 2),
        Coordinate(2, 2),
    ]:
        assert n in neighbors


@test(
    "MooreCell: A cell located at the top left of a matrix will have neighbors that wrap to the \
other side",
)
def _() -> None:
    c = MooreCell(Coordinate(0, 0))
    neighbors = c.get_neighbors(max_coord())
    assert all(
        n in neighbors
        for n in [
            Coordinate(2, 2),
            Coordinate(0, 2),
            Coordinate(2, 0),
            Coordinate(1, 2),
            Coordinate(1, 0),
            Coordinate(1, 1),
            Coordinate(0, 1),
            Coordinate(2, 1),
        ]
    )


@test(
    "MooreCell: A cell located at the bottom right of a matrix will have neighbors that wrap to \
the other side",
)
def _() -> None:
    c = MooreCell(Coordinate(2, 2))
    neighbors = c.get_neighbors(max_coord())
    assert all(
        n in neighbors
        for n in [
            Coordinate(2, 1),
            Coordinate(0, 1),
            Coordinate(0, 2),
            Coordinate(0, 0),
            Coordinate(2, 0),
            Coordinate(1, 0),
            Coordinate(1, 2),
        ]
    )


@test(
    "NeumannCell: A cell located at the top left of a matrix will have neighbors that wrap to the \
other side",
)
def _() -> None:
    c = NeumannCell(Coordinate(0, 0))
    neighbors = c.get_neighbors(max_coord())
    assert all(n in neighbors for n in [Coordinate(0, 2), Coordinate(2, 0)])


@test(
    "NeumannCell: A cell located at the bottom right of a matrix will have neighbors that wrap to \
the other side",
)
def _() -> None:
    c = MooreCell(Coordinate(2, 2))
    neighbors = c.get_neighbors(max_coord())
    assert all(n in neighbors for n in [Coordinate(2, 0), Coordinate(0, 2)])
