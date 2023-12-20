"""A module for storing commonly used scenarios"""

import random

from rich.console import Console

from .coordinate import Coordinate
from .simulation import Simulation
from .cell import MooreCell, MooreCellState


def get_dimensions():
    """Gets the xmax and ymax for the terminal's dimensions"""
    console = Console()
    xmax = console.width
    ymax = console.height * 2
    return (xmax, ymax)


def moore_nbhd_1() -> Simulation:
    xmax, ymax = get_dimensions()
    sim = Simulation(xmax, ymax)
    states = (MooreCellState.ON, MooreCellState.OFF)
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            state = states[random.randint(0, 1)]
            cell = MooreCell(Coordinate(x, y), state, sim.matrix)
            sim.spawn(cell)
    return sim


def moore_nbhd_2() -> Simulation:
    xmax, ymax = get_dimensions()
    sim = Simulation(xmax, ymax)
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            r = random.randint(0, 10)
            if r > 9:
                state = MooreCellState.ON
            else:
                state = MooreCellState.OFF
            cell = MooreCell(Coordinate(x, y), state, sim.matrix)
            sim.spawn(cell)
    return sim


MOORE_NBHD_1 = moore_nbhd_1()
MOORE_NBHD_2 = moore_nbhd_2()
