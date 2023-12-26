import time
from copy import copy
from dataclasses import dataclass
from typing import List, Optional, Type, Union

from rich.console import Console, ConsoleOptions, RenderResult
from rich.live import Live
from rich.segment import Segment
from rich.style import Style

from .cell import Cell
from .coordinate import Coordinate
from .matrix import Matrix2D
from .state import CellState


@dataclass
class StateData:
    """Used to simplify access of neighbors and state data in the Simulation class

    Args:
        neighbors (List[Coordinate]): A list of the neighbor's coordinates to access
        state (CellState): An instance of a a CellState
    """

    neighbors: List[Coordinate]
    state: CellState


class Simulation:
    """A class to run a simulation from the terminal

    Attributes:
        1. matrix (CellMatrix): The underlying cell matrix
    """

    def __init__(self, cell_type: Type[Cell], initial_state: CellState) -> None:
        """Initializes an instance of the Simulation class

        Args:
            cell_type (Type[Cell]): The type of cell the simulation should use when determining neighbors
            initial_state (CellState): The initial state of a cell the matrix should be filled with
        """

        console = Console()
        xmax = console.width
        ymax = console.height * 2

        self.matrix = Matrix2D(xmax, ymax)
        for y in range(self.ymax + 1):
            for x in range(self.xmax + 1):
                coord = Coordinate(x, y)
                c = cell_type(Coordinate(x, y))
                neighbors = c.get_neighbors(self.matrix.max_coord)
                state = initial_state
                self.matrix[coord] = StateData(neighbors, state)

    @property
    def xmax(self) -> int:
        """Interface to access the max x coordinate of the underlying matrix

        Returns
            The max y coordinate of the underlying matrix
        """
        return self.matrix.xmax

    @property
    def ymax(self) -> int:
        """Interface to access the max y coordinate of the underlying matrix

        Returns
            The max y coordinate of the underlying matrix
        """
        return self.matrix.ymax

    @property
    def max_coord(self) -> Coordinate:
        """Interface to access the max coordinate of the underlying matrix

        Returns
            The max coordinate of the underlying matrix
        """

        return self.matrix.max_coord

    @property
    def midpoint(self) -> Coordinate:
        return self.matrix.midpoint

    def set_state(self, coord: Coordinate, state: CellState) -> None:
        """Spawns a CellState instance at a given x/y coordinate

        Args:
            coord (Coordinate): The coordinate to spawn a cell state at
            cell (Cell): An object which conforms to the Cell protocol
        """

        self.matrix[coord].state = state

    def spawn(self, midpoint: Coordinate, pattern: Matrix2D):
        for y in range(pattern.ymax + 1):
            for x in range(pattern.xmax + 1):
                coord = Coordinate(x, y)
                offset = Coordinate(x, y) + midpoint
                self.set_state(offset, pattern[coord])

    def start(
        self,
        refresh_rate: int = 0,
        duration: Union[float, int] = 0,
        render: Optional[bool] = True,
        debug=False,
    ) -> None:
        """Sets initial parameters for the simluation, then runs it

        Args:
            duration (Union[float, int]): The duration the simulation should run for. Defaults to 0 (infinity)
            refresh_rate (int): The number of times the simluation should run before sleeping. Defaults to 0
            render (bool): Controls if the simulation renders to the terminal. Defaults to True
            debug (bool): Controls if the simulation runs in debug mode. This will run cProfile and disable rendering
        """
        if refresh_rate == 0:
            sleep = 0.0
        else:
            sleep = 1 / refresh_rate

        if duration == 0:
            duration = float("inf")

        if debug is True:
            import cProfile

            cProfile.runctx(
                "exec(self.run(duration, sleep, False))", globals(), locals()
            )

        elif render is True:
            self.run(duration, sleep, True)

        else:
            self.run(duration, sleep, False)

    def run(
        self,
        duration: Union[float, int],
        sleep: Union[float, int],
        render: bool,
    ) -> None:
        """Runs the simulation

        Args:
            duration (Union[float, int]): The duration the simulation should run for
            sleep (Union[float, int]): The time the simulation should sleep between each step
            render: bool: Cotnrols if the simulation renders to the terminal
        """
        elapsed = 0
        if render is True:
            with Live(self, screen=True, auto_refresh=False) as live:
                while elapsed < duration:
                    self.step()
                    live.update(self, refresh=True)
                    time.sleep(sleep)
                    elapsed += 1
        else:
            while elapsed < duration:
                self.step()
                time.sleep(sleep)
                elapsed += 1

    def step(self) -> None:
        """Steps the simulation forward once

        Visits each cell in the 2d matrix and retrieves its new state by passing its neighbor states to the change_state
        method.
        """
        ref = copy(self.matrix)
        for y in range(self.matrix.ymax + 1):
            for x in range(self.matrix.xmax + 1):
                coord = Coordinate(x, y)
                data = ref[coord]
                neighbor_states = []
                for nc in data.neighbors:
                    neighbor_state = ref[nc].state
                    neighbor_states.append(neighbor_state)
                new = data.state.change_state(neighbor_states)
                self.matrix[coord].state = new

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Renders each Cell in the simulation using the Rich Console Protocol

        Due to the typical 2:1 height/width aspect ratio of a terminal, each cell rendered from the CellMatrix simulation
        actually occupies 2 rows in the terminal. I picked up this trick from rich's __main__ module. Run
        'python -m rich and observe the color palette at the top of stdout for another example of what this refers to.

        Yields:
            2 cells in the simulation, row by row, until all cell states have been rendered.
        """
        for y in range(self.matrix.max_coord.y)[::2]:
            for x in range(self.matrix.max_coord.x + 1):
                bg = self.matrix[Coordinate(x, y)].state.color
                fg = self.matrix[Coordinate(x, y + 1)].state.color
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()
