"""Contains classes and functionality related to cell states."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Protocol, Self

from .color import Color

if TYPE_CHECKING:
    from collections.abc import Sequence


class CellState(Protocol):
    """A protocol to reference when creating a new type of cell state."""

    # colors should be a tuple of colors equivalent to the number of possible states in a CellState
    # class
    colors: Sequence[Color]

    @property
    def color(self) -> Color:
        """Correlate a color with arbitrary attributes of a CellState instance.

        Returns:
            A valid color designator (can be 'red', hex codes, etc. See the rich documentation
            for details)

        """

    @classmethod
    def set_colors(cls, colors: list[Color]) -> None:
        """Set the colors for the CellState."""

    def change_state(self, neighbors: list[Self]) -> CellState:
        """Retrieve a new state based on its neighbors.

        Returns:
            The cell's new state

        """


class ConwayState:
    """A state that follows the rules for Conway's Game of Life.

    Attributes:
        colors (Tuple[Color, Color]): A tuple of colors (see Textualize's documentation for 'rich'
        for accepted values). The first index is the color for ALIVE states. 2nd is DEAD
        birth_rules (list[int]): A list of integers representing the rules for a cell to become
        "resurrected"
        survival_rules (list[int]): A list of integers representing the rules for a cell to stay
        alive
        alive (bool): Flag for whether the cell is ALIVE (True) or DEAD (False)

    """

    colors: Sequence[Color] = [Color("#F6AE2D"), Color("#315771")]
    birth_rules: ClassVar[list[int]] = [3]
    survival_rules: ClassVar[list[int]] = [2, 3]

    def __init__(
        self,
        alive: bool = False,
    ) -> None:
        """Initialize an instance of the ConwayState class.

        Args:
            colors (Tuple[Color, Color]): A tuple of colors (see Textualize's documentation for
            'rich' for accepted values). The first index is the color for ALIVE states. 2nd is DEAD
            alive (bool): Flag for whether the cell is ALIVE (True) or DEAD (False)

        """
        self.alive = alive

    @property
    def color(self) -> Color:
        """Return the first index of self.colors if alive, else the second."""
        if self.alive is True:
            return self.colors[0]
        return self.colors[1]

    @classmethod
    def set_colors(cls, colors: list[Color]) -> None:
        """Set the colors for the CellState.

        Args:
            colors (List[Color]): The list of colors to change to

        """
        if len(colors) < len(ConwayState.colors):
            colors.extend(ConwayState.colors[len(colors) :])
        elif len(colors) > len(ConwayState.colors):
            colors = colors[: len(ConwayState.colors)]

        cls.colors = colors

    def change_state(self, neighbors: list[ConwayState]) -> ConwayState:
        """Change the state of the cell.

        An instance of this class will follow birth/survival rules according to the
        ConwayState.birth_rules and ConwayState.survival_rules class attributes. Default rules are
        B3/S23.

        Args:
            neighbors (List[ConwayState]): A list of neighbor's states

        Returns:
            The cell's new state

        """
        alive_count = 0
        for n in neighbors:
            if n.alive is True:
                alive_count += 1

        match self.alive:
            case True:
                if any(alive_count == r for r in self.survival_rules):
                    return ConwayState(alive=True)
                return ConwayState(alive=False)

            case False:
                if any(alive_count == r for r in self.birth_rules):
                    return ConwayState(alive=True)
                return ConwayState(alive=False)
