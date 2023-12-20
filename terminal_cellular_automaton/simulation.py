from __future__ import annotations

from time import sleep
from typing import Optional, Union

from rich.console import Console
from rich.live import Live

from .coordinate import Coordinate
from .matrix import CellMatrix


class Simulation:
    """A class to run a simulation from the terminal

    Default behavior is to run the simulation at the current dimensions of the terminal. Currently, this is not
    modifiable by the user without direct interference with the underlying matrix attr

    Attributes:
        1. matrix (CellMatrix): The underlying cell matrix
    """

    def __init__(self, xmax: Optional[int] = None, ymax: Optional[int] = None) -> None:
        """Initializes an instance of the Simulation class"""

        if xmax is None or ymax is None:
            console = Console()
            if xmax is None:
                xmax = console.width
            if ymax is None:
                ymax = console.height * 2

        self.matrix = CellMatrix(xmax, ymax)

    @property
    def xmax(self):
        return self.matrix.max_coord.x

    @property
    def ymax(self):
        return self.matrix.max_coord.y

    def spawn(self, element) -> None:
        """Spawns an element at a given x/y coordinate

        Args:
            element (ElementType): An 'ElementType' type
            coord (Coordinate): The coordinate to spawn the element at
        """

        self.matrix[element.coord] = element

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
            sleep_for = 0
        else:
            sleep_for = 1 / refresh_rate

        if duration == 0:
            duration = float("inf")

        if debug is True:
            import cProfile

            cProfile.runctx(
                "exec(self.run(duration, sleep_for, False))", globals(), locals()
            )

        elif render is True:
            self.run(duration, sleep_for, True)

        else:
            self.run(duration, sleep_for, False)

    def run(
        self,
        duration: Union[float, int],
        sleep_for: Union[float, int],
        render: bool,
    ) -> None:
        """Runs the simulation

        Args:
            duration (Union[float, int]): The duration the simulation should run for
            sleep_for (Union[float, int]): The time the simulation should sleep between each step
            render: bool: Cotnrols if the simulation renders to the terminal
        """
        elapsed = 0
        if render is True:
            with Live(self.matrix, screen=True, auto_refresh=False) as live:
                while elapsed < duration:
                    self.step()
                    live.update(self.matrix, refresh=True)
                    sleep(sleep_for)
                    elapsed += 1
        else:
            while elapsed < duration:
                self.step()
                sleep(sleep_for)
                elapsed += 1

    def step(self) -> None:
        """Steps the simulation forward once

        Explores every element in the simulation by working bottom to top, then left -> middle; right -> middle for each
        row. Each step in the simulation calls the 'step' method on the underlying Cell type. Cell.step will determien
        its next place in the CellMatrix and modify the CellMatrix reference passed to it accordingly.

        Issue:
            When we step each element from left -> right or right -> left, the elements on the trailing end exhibit odd
            behavior. Specifically, elements will move diagonally and to the left (or right) depending on the order
            we're stepping them in. Unsure of the exact cause of this, but for now, working "middle out" in either
            direction visually solves the problem. This probably means there's some odd behavior in the middle of the
            matrix for each step, but it's not visually identifiable. Working "middle out" is an acceptable workaround
            for now.

        After each cell has been stepped through, reset its updated flag to False
        """
        for y in range(self.matrix.max_coord.y + 1):
            row = self.matrix.max_coord.y - y
            for x in range(self.matrix.max_coord.x + 1):
                cell = self.matrix[Coordinate(x, row)]
                cell.change_state(self.matrix)
