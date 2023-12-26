"""A module for storing commonly used scenarios"""

import random
from collections import namedtuple

from . import patterns
from .cell import MooreCell
from .coordinate import Coordinate
from .simulation import Simulation
from .state import ConwayState

Box = namedtuple("Box", ["top_left", "top_right", "bottom_left", "bottom_right"])


def conway_1() -> Simulation:
    sim = Simulation(MooreCell, ConwayState(False))
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            alive = bool(random.randint(0, 1))
            coord = Coordinate(x, y)
            s = ConwayState(alive)
            sim.set_state(coord, s)
    return sim


def conway_2() -> Simulation:
    sim = Simulation(MooreCell, ConwayState(False))
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            coord = Coordinate(x, y)
            r = random.randint(0, 10)
            if r > 9:
                alive = True
            else:
                alive = False
            s = ConwayState(alive)
            sim.set_state(coord, s)
    return sim


def pulsar() -> Simulation:
    sim = Simulation(MooreCell, ConwayState(False))
    pulsar = patterns.Pulsar()
    sim.spawn(sim.midpoint - pulsar.midpoint, pulsar)
    return sim


def glider() -> Simulation:
    sim = Simulation(MooreCell, ConwayState(False))
    glider = patterns.Glider()
    sim.spawn(glider.midpoint, glider)
    return sim


CONWAY_1 = conway_1()
CONWAY_2 = conway_2()
PULSAR = pulsar()
GLIDER = glider()
