import time
from copy import copy
from typing import Optional, Union, Generic, TypeVar, Type

from rich.console import Console, ConsoleOptions, RenderResult
from rich.live import Live
from rich.segment import Segment
from rich.style import Style

from .cell import Cell
from .state import CellState
from .coordinate import Coordinate
from .matrix import Matrix2D
from rich.console import Console
from dataclasses import dataclass

S = TypeVar("S", bound=CellState)


@dataclass
class StateData:
    neighbors: list[Coordinate]
    state: CellState


class Simulation(Generic[S]):
    """A class to run a simulation from the terminal

    Attributes:
        1. matrix (CellMatrix): The underlying cell matrix
    """

    def __init__(self, cell_type: Type[Cell], initial_state: S) -> None:
        """Initializes an instance of the Simulation class"""

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
    def xmax(self):
        return self.matrix.max_coord.x

    @property
    def ymax(self):
        return self.matrix.max_coord.y

    @property
    def max_coord(self):
        return self.matrix.max_coord

    def spawn(self, coord: Coordinate, state: S) -> None:
        """Spawns a cell at a given x/y coordinate

        Args:
            cell (Cell): An object which conforms to the Cell protocol
        """

        self.matrix[coord].state = state

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

        Visits each cell in the 2d matrix and executes its 'change_state' method
        """
        ref = copy(self.matrix)
        for y in range(self.matrix.max_coord.y + 1):
            for x in range(self.matrix.max_coord.x + 1):
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
