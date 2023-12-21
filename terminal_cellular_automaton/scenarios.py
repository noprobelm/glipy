"""A module for storing commonly used scenarios"""

import random

from . import cell, states
from .coordinate import Coordinate
from .simulation import Simulation
from collections import namedtuple

Box = namedtuple("Box", ["top_left", "top_right", "bottom_left", "bottom_right"])


def conway_1() -> Simulation:
    sim = Simulation()
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            alive = bool(random.randint(0, 1))
            c = cell.MooreCell(
                Coordinate(x, y),
                sim.max_coord,
                states.ConwayState(("green", "red"), alive),
            )
            sim.spawn(c)
    return sim


def conway_2() -> Simulation:
    sim = Simulation()
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            r = random.randint(0, 10)
            if r > 9:
                alive = True
            else:
                alive = False
            c = cell.MooreCell(
                Coordinate(x, y),
                sim.max_coord,
                states.ConwayState(("green", "red"), alive),
            )
            sim.spawn(c)
    return sim


def pulsar() -> Simulation:
    sim = Simulation()
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            c = cell.MooreCell(
                Coordinate(x, y),
                sim.max_coord,
                states.ConwayState(("green", "red"), False),
            )
            sim.spawn(c)

    midpoint = Coordinate(sim.xmax // 2, sim.ymax // 2)
    top_left = Coordinate(midpoint.x - 7, midpoint.y - 7)
    state = states.ConwayState(("green", "red"), True)
    row = top_left + Coordinate(0, 3)
    for x in range(4, 7):
        c = cell.MooreCell(row + Coordinate(x, 0), sim.max_coord, state)
        sim.spawn(c)
        c = cell.MooreCell(row + Coordinate(x + 6, 0), sim.max_coord, state)
        sim.spawn(c)

    row = top_left + Coordinate(0, 8)
    for x in range(4, 7):
        c = cell.MooreCell(row + Coordinate(x, 0), sim.max_coord, state)
        sim.spawn(c)
        c = cell.MooreCell(row + Coordinate(x + 6, 0), sim.max_coord, state)
        sim.spawn(c)

    row = top_left + Coordinate(0, 10)
    for x in range(4, 7):
        c = cell.MooreCell(row + Coordinate(x, 0), sim.max_coord, state)
        sim.spawn(c)
        c = cell.MooreCell(row + Coordinate(x + 6, 0), sim.max_coord, state)
        sim.spawn(c)

    row = top_left + Coordinate(0, 15)
    for x in range(4, 7):
        c = cell.MooreCell(row + Coordinate(x, 0), sim.max_coord, state)
        sim.spawn(c)
        c = cell.MooreCell(row + Coordinate(x + 6, 0), sim.max_coord, state)
        sim.spawn(c)

    for y in [5, 6, 7, 11, 12, 13]:
        for x in (2, 7, 9, 14):
            for _ in range(4):
                c = cell.MooreCell(top_left + Coordinate(x, y), sim.max_coord, state)
                sim.spawn(c)

    return sim


CONWAY_1 = conway_1()
CONWAY_2 = conway_2()
PULSAR = pulsar()
