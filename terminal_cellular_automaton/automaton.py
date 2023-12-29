from __future__ import annotations
import time
from copy import copy
from dataclasses import dataclass
from typing import List, Optional, Type, Union, Sequence

from rich.console import Console, ConsoleOptions, RenderResult
from rich.live import Live
from rich.segment import Segment
from rich.style import Style

from .cell import Cell
from .coordinate import Coordinate
from .state import CellState


@dataclass
class StateData:
    """Used to simplify access of neighbors and state data in an Automaton instance

    Args:
        neighbors (List[Coordinate]): A list of the neighbor's coordinates to access
        state (CellState): An instance of a a CellState
    """

    neighbors: List[Coordinate]
    state: CellState


class Automaton:
    """Hosts the data and methods to store/evolve an automaton

    Attributes:
        xmax (int): The maximum x coordinate
        ymax (int): The maximum y coordinate
        max_coord (Coordinate): The maximum valid coordinate found in the grid
        midpoint (Coordinate): The midpoint of the matrix
        matrix (CellMatrix): The underlying cell matrix
    """

    def __init__(
        self,
        cell_type: Type[Cell],
        initial_state: Union[CellState, Sequence[Sequence[CellState]]],
        xmax: Optional[int] = None,
        ymax: Optional[int] = None,
    ) -> None:
        """Initializes an instance of the Simulation class

        Args:
            cell_type (Type[Cell]): The type of cell the simulation should use when determining neighbors
            initial_state (CellState): The initial state of a cell the matrix should be filled with
        """

        self._cell_type = cell_type
        if xmax is None or ymax is None:
            console = Console()
            if xmax is None:
                self.xmax = console.width
            if ymax is None:
                self.ymax = console.height * 2
        else:
            self.xmax = xmax
            self.ymax = ymax

        self.max_coord = Coordinate(self.xmax, self.ymax)
        self.midpoint = Coordinate(self.xmax // 2, self.ymax // 2)

        self.matrix: List[List[StateData]] = []

        if isinstance(initial_state, list):
            for y in range(self.ymax + 1):
                self.matrix.append([])
                for x in range(self.xmax + 1):
                    coord = Coordinate(x, y)
                    c = self._cell_type(coord)
                    neighbors = c.get_neighbors(self.max_coord)
                    state = initial_state[y][x]
                    self.matrix[y].append(StateData(neighbors, state))
        else:
            for y in range(self.ymax + 1):
                self.matrix.append([])
                for x in range(self.xmax + 1):
                    coord = Coordinate(x, y)
                    c = self._cell_type(coord)
                    neighbors = c.get_neighbors(self.max_coord)
                    self.matrix[y].append(StateData(neighbors, initial_state))

    def set_state(self, coord: Coordinate, state: CellState) -> None:
        """Spawns a CellState instance at a given x/y coordinate

        Args:
            coord (Coordinate): The coordinate to spawn a cell state at
            cell (Cell): An object which conforms to the Cell protocol
        """

        self.matrix[coord.y][coord.x].state = state

    def spawn(self, midpoint: Coordinate, pattern: Automaton):
        for y in range(pattern.ymax + 1):
            for x in range(pattern.xmax + 1):
                coord = Coordinate(x, y)
                offset = Coordinate(x, y) + midpoint
                self.set_state(offset, pattern.matrix[coord.y][coord.x].state)

    def start(
        self,
        refresh_rate: int = 30,
        generations: Union[float, int] = 0,
        render: Optional[bool] = True,
        debug=False,
    ) -> None:
        """Sets initial parameters for the simluation, then runs it

        Args:
            generation (Union[float, int]): The number of generations the simulation should run for. Defaults to 0 (infinity)
            refresh_rate (int): The number of times the simluation should run before sleeping. Defaults to 0
            render (bool): Controls if the simulation renders to the terminal. Defaults to True
            debug (bool): Controls if the simulation runs in debug mode. This will run cProfile and disable rendering
        """
        if refresh_rate == 0:
            sleep = 0.0
        else:
            sleep = 1 / refresh_rate

        if generations == 0:
            generations = float("inf")

        if debug is True:
            import cProfile

            cProfile.runctx(
                "exec(self.run(duration, sleep, False))", globals(), locals()
            )

        elif render is True:
            self.run(generations, sleep, True)

        else:
            self.run(generations, sleep, False)

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
                    self.evolve()
                    live.update(self, refresh=True)
                    time.sleep(sleep)
                    elapsed += 1
        else:
            while elapsed < duration:
                self.evolve()
                time.sleep(sleep)
                elapsed += 1

    def evolve(self) -> None:
        """Steps the simulation forward once

        Visits each cell in the 2d matrix and retrieves its new state by passing its neighbor states to the change_state
        method.
        """
        ref = copy(self)
        for y in range(self.ymax + 1):
            for x in range(self.xmax + 1):
                coord = Coordinate(x, y)
                data = ref.matrix[coord.y][coord.x]
                neighbor_states = []
                for nc in data.neighbors:
                    neighbor_state = ref.matrix[nc.y][nc.x].state
                    neighbor_states.append(neighbor_state)
                new = data.state.change_state(neighbor_states)
                self.matrix[coord.y][coord.x].state = new

    def __copy__(self) -> Automaton:
        """Returns a shallow copy of an instance

        Returns:
            A shallow copy of a Matrix2D instance
        """
        matrix = []
        for y in range(self.ymax + 1):
            matrix.append([])
            for x in range(self.xmax + 1):
                matrix[y].append(copy(self.matrix[y][x]))
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update({"matrix": matrix})
        return result

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
        for y in range(self.max_coord.y)[::2]:
            for x in range(self.max_coord.x + 1):
                bg = self.matrix[y][x].state.color
                fg = self.matrix[y + 1][x].state.color
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()
