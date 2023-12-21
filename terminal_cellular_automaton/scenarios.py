"""A module for storing commonly used scenarios"""

import random

from rich.console import Console

from . import cell, states
from .coordinate import Coordinate
from .simulation import Simulation


def _get_dimensions():
    """Gets the xmax and ymax for the terminal's dimensions"""
    console = Console()
    xmax = console.width
    ymax = console.height * 2
    return (xmax, ymax)


def conway_1() -> Simulation:
    xmax, ymax = _get_dimensions()
    sim = Simulation(xmax, ymax)
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            alive = bool(random.randint(0, 1))
            c = cell.MooreCell(
                Coordinate(x, y),
                states.ConwayState(("green", "red"), alive),
            )
            sim.spawn(c)
    return sim


def conway_2() -> Simulation:
    xmax, ymax = _get_dimensions()
    sim = Simulation(xmax, ymax)
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            r = random.randint(0, 10)
            if r > 9:
                alive = True
            else:
                alive = False
            c = cell.MooreCell(
                Coordinate(x, y),
                states.ConwayState(("green", "red"), alive),
            )
            sim.spawn(c)
    return sim


CONWAY_1 = conway_1()
CONWAY_2 = conway_2()
