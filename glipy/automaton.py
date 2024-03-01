"""This module contains the Automaton class, which is the base class for all cellular automata in glipy"""

from __future__ import annotations

import cProfile
import sys
import time
from dataclasses import dataclass
from typing import Generic, List, Sequence, Type, TypeVar, Union, cast

from .cell import Cell
from .coordinate import Coordinate
from .state import CellState

C = TypeVar("C", bound=Cell)
S = TypeVar("S", bound=CellState)


@dataclass
class StateData:
    """Used to simplify access of neighbors and state data in an Automaton instance

    Args:
        neighbors (List[Coordinate]): A list of the neighbor's coordinates to access
        state (CellState): An instance of a a CellState
    """

    neighbors: List[Coordinate]
    state: CellState


class Automaton(Generic[C, S]):
    """Hosts the data and methods to store/evolve an automaton.

    An automaton's cell and cell_state types must be homogenous for the duration of its existence to ensure a cell_state
    is always aware of how it should behave with respect to its provided neighbors. The generics 'C' and 'S' in the class
    signature enforce this.

    Attributes:
        generation (int): The generation we're at in the simulation
        cell_type (Type[Cell]) The type of Cell the automaton is working with
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
        xmax: int,
        ymax: int,
    ) -> None:
        """Initializes an instance of the Simulation class

        Args:
            cell_type (Type[Cell]): The type of cell the simulation should use when determining neighbors
            initial_state (CellState): The initial state of a cell the matrix should be filled with
            xmax (Optional[int]): The xmax value to use for the automaton
            ymax (Optional[int]): The ymax value to use for the automaton
        """

        self.generation = 0
        self.cell_type = cell_type
        self.xmax = xmax
        self.ymax = ymax

        self.max_coord = Coordinate(self.xmax, self.ymax)
        self.midpoint = Coordinate(self.xmax // 2, self.ymax // 2)

        self.matrix: List[List[StateData]] = []

        if isinstance(initial_state, list):
            self._state_type = type(initial_state[0][0])
            for y in range(self.ymax + 1):
                self.matrix.append([])
                for x in range(self.xmax + 1):
                    coord = Coordinate(x, y)
                    c = self.cell_type(coord)
                    neighbors = c.get_neighbors(self.max_coord)
                    state = initial_state[y][x]
                    self.matrix[y].append(StateData(neighbors, state))
        else:
            # I don't like this [cast] solution very much, but mypy and our code analysis tools should catch improper arg
            # usage upstream from here. If we don't use cast here, 'initial_state' is considered to be ambiguous in its
            # type (Union[CellState, Sequence[Sequence[CellState]]]), which is incompatable with the StateData 'state'
            # attribute. We've already verified 'initial_state' is not a sequence from our conditional logic above, so
            # if we're here it must be CellState compliant.
            initial_state = cast(CellState, initial_state)
            self._state_type = type(initial_state)
            for y in range(self.ymax + 1):
                self.matrix.append([])
                for x in range(self.xmax + 1):
                    coord = Coordinate(x, y)
                    c = self.cell_type(coord)
                    neighbors = c.get_neighbors(self.max_coord)
                    self.matrix[y].append(StateData(neighbors, initial_state))

    def evolve(self) -> None:
        """Evolves the simulation once

        Visits each cell in the 2d matrix and retrieves its new state by passing its neighbor states to the change_state
        method.
        """
        next_generation: List[List[StateData]] = []
        for y in range(self.ymax + 1):
            next_generation.append([])
            for x in range(self.xmax + 1):
                coord = Coordinate(x, y)
                data = self.matrix[coord.y][coord.x]
                neighbor_states = []
                for nc in data.neighbors:
                    neighbor_state = self.matrix[nc.y][nc.x].state
                    neighbor_states.append(neighbor_state)
                new_state = data.state.change_state(neighbor_states)
                next_generation[y].append(StateData(data.neighbors, new_state))

        self.matrix = next_generation
        self.generation += 1

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

    def clear(self):
        """Sets the Automaton's underlying matrix to the default state type"""
        for y in range(self.ymax + 1):
            for x in range(self.xmax + 1):
                self.matrix[y][x].state = self._state_type()

    def run(
        self,
        refresh_rate: int = 30,
        generations: Union[float, int] = 0,
        debug: bool = False,
    ) -> None:
        """Sets initial parameters for the simluation, then runs it

        Args:
            generations (Union[float, int]): The number of generations the simulation should run for. Defaults to 0 (infinity)
            refresh_rate (int): The number of times the simluation should run before sleeping. Defaults to 0
            debug (bool): Controls if the simulation runs in debug mode. This will run cProfile and disable rendering
        """
        if debug is True:
            cProfile.runctx(
                "eval('self.run(refresh_rate, generations, False)')",
                globals(),
                locals(),
            )

        if refresh_rate == -1:
            sleep = 0.0
        elif refresh_rate == 0:
            sleep = float("inf")
        else:
            sleep = 1 / refresh_rate

        if generations == 0:
            generations = float("inf")

        try:
            if sleep == float("inf"):
                while True:
                    time.sleep(1)

            while self.generation < generations:
                self.evolve()
                time.sleep(sleep)

        except KeyboardInterrupt:
            sys.exit(0)

    @property
    def colors(self) -> Sequence[str]:
        """For renderers, this property can be used to retrieve a state type's colors

        Returns:
            The colors being used for the cell state
        """
        # Ignoring for pyright. Mypy has no issue with this line.
        return self._state_type.colors  # type: ignore

    @colors.setter
    def colors(self, colors: List[str]) -> None:
        """Sets the colors being used for htis instance's cell state type

        Args:
            colors (List[str]): The colors to use

        """
        self._state_type.set_colors(colors)
