"""A module for storing commonly used scenarios"""

import random
from collections import namedtuple

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
            sim.spawn(coord, s)
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
            sim.spawn(coord, s)
    return sim


def pulsar() -> Simulation:
    sim = Simulation(MooreCell, ConwayState(False))
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            coord = Coordinate(x, y)
            s = ConwayState(alive=False)
            sim.spawn(coord, s)

    midpoint = Coordinate(sim.xmax // 2, sim.ymax // 2)
    top_left = Coordinate(midpoint.x - 7, midpoint.y - 7)
    state = ConwayState(alive=True)
    row = top_left + Coordinate(0, 3)
    for x in range(4, 7):
        coord = row + Coordinate(x, 0)
        sim.spawn(coord, state)

        coord = row + Coordinate(x + 6, 0)
        sim.spawn(coord, state)

    row = top_left + Coordinate(0, 8)
    for x in range(4, 7):
        coord = row + Coordinate(x, 0)
        sim.spawn(coord, state)

        coord = row + Coordinate(x + 6, 0)
        sim.spawn(coord, state)

    row = top_left + Coordinate(0, 10)
    for x in range(4, 7):
        coord = row + Coordinate(x, 0)
        sim.spawn(coord, state)
        coord = row + Coordinate(x + 6, 0)
        sim.spawn(coord, state)

    row = top_left + Coordinate(0, 15)
    for x in range(4, 7):
        coord = row + Coordinate(x, 0)
        sim.spawn(coord, state)

        coord = row + Coordinate(x + 6, 0)
        sim.spawn(coord, state)

    for y in [5, 6, 7, 11, 12, 13]:
        for x in (2, 7, 9, 14):
            for _ in range(4):
                coord = top_left + Coordinate(x, y)
                sim.spawn(coord, state)

    return sim


CONWAY_1 = conway_1()
CONWAY_2 = conway_2()
PULSAR = pulsar()
