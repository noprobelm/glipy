"""Use this module to create commonly accessed patterns"""

from typing import List, Sequence, Type, Self, Union
from pathlib import Path

from . import reader
from .automaton import Automaton
from .cell import Cell, MooreCell
from .coordinate import Coordinate
from .state import CellState, ConwayState


class Pattern(Automaton):
    """A boilerplate Pattern class. All patterns should derive from this class.

    A pattern is itself simply an Automaton. The Automaton.spawn() method can be used to spawn other Automaton objects
    at a specified position.

    Like the Automaton class, this class is agnostic to the cell/state types it works with. Additional subclasses
    should be created for dealing with specific cell/state types
    """

    def __init__(
        self,
        cell_type: Type[Cell],
        states: Sequence[Sequence[CellState]],
        xmax: int,
        ymax: int,
    ):
        super().__init__(cell_type, states, xmax, ymax)


class ConwayPattern(Pattern):
    """A boilerplate Pattern class for Conway patterns"""

    def __init__(self, states: Sequence[Sequence[ConwayState]], xmax: int, ymax: int):
        super().__init__(MooreCell, states, xmax, ymax)

    @staticmethod
    def fill_dead(
        xmax: int, ymax: int, alive: Sequence[Coordinate]
    ) -> List[List[ConwayState]]:
        """Convenience method for filling in dead cell states based on coordinates of staes known to ba alive

        Args:
            xmax (int): The maximum x coordinate of a pattern
            ymax (int): The maximum y coordinate of a pattern
            alive (Sequence[Coordinate]): A sequence of coordinates of cells known to be alive

        Returns:
            List[List[ConwayState]]: A 2d list representative of a cellular automaton
        """

        states: List[List[ConwayState]] = []
        for y in range(ymax + 1):
            states.append([])
            for x in range(xmax + 1):
                if Coordinate(x, y) in alive:
                    states[y].append(ConwayState(True))
                else:
                    states[y].append(ConwayState(False))

        return states

    @classmethod
    def from_life(cls, path: Union[Path, str]) -> Self:
        """Builds a pattern from 'life' data compliant with life version 1.06 read from a file

        Args:
            data (str): The lines from a file compliant with life 1.06 standards

        Returns:
            A ConwayPattern based on 'life' data
        """
        pattern = reader.life(path)
        return pattern

    @classmethod
    def from_rle(cls, path: Union[Path, str]) -> Self:
        """Builds a pattern from compliant Run Length Encoded (RLE) data read from a file.

        Args:
            data (List[str]): The lines from a file compliant with RLE standards

        Returns:
            A ConwayPattern based on 'rle' data
        """
        pattern = reader.rle(path)
        return pattern


class Glider(ConwayPattern):
    """A glider pattern"""

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

        states = self.fill_dead(xmax, ymax, alive)
        super().__init__(states, xmax, ymax)


class Pulsar(ConwayPattern):
    """A pulsar pattern"""

    def __init__(self):
        xmax = 12
        ymax = 12
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
        states = self.fill_dead(xmax, ymax, alive)
        super().__init__(states, xmax, ymax)


class CloverLeaf(ConwayPattern):
    """A CloverLeaf pattern"""

    def __init__(self):
        xmax = 8
        ymax = 10
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

        states = self.fill_dead(xmax, ymax, alive)
        super().__init__(states, xmax, ymax)
