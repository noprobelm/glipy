"""A module for storing commonly used scenarios"""

import random

from . import patterns
from .cell import MooreCell
from .coordinate import Coordinate
from .simulation import Simulation
from .state import ConwayState


def conway_1() -> Simulation:
    """A random game, where each cell has a 1 in 2 chance of spawning as alive"""
    sim = Simulation(MooreCell, ConwayState(False))
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            alive = bool(random.randint(0, 1))
            coord = Coordinate(x, y)
            s = ConwayState(alive)
            sim.set_state(coord, s)
    return sim


def conway_2() -> Simulation:
    """A random game, where each cell has a 1 in 10 chance of spawning as alive"""
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
    """A pulsar life generated from the patterns module"""
    sim = Simulation(MooreCell, ConwayState(False))
    pulsar = patterns.Pulsar()
    sim.spawn(sim.midpoint - pulsar.midpoint, pulsar)
    return sim


def glider() -> Simulation:
    """A glider life generated from the patterns module"""
    sim = Simulation(MooreCell, ConwayState(False))
    glider = patterns.Glider()
    sim.spawn(glider.midpoint, glider)
    return sim


def clover_leaf() -> Simulation:
    """A clover leaf generated from the patterns module"""
    sim = Simulation(MooreCell, ConwayState(False))
    leaf = patterns.CloverLeaf()
    sim.spawn(sim.midpoint - leaf.midpoint, leaf)
    return sim


def domino_sparker() -> Simulation:
    """A domino sparker generated from an rle file"""
    sim = Simulation(MooreCell, ConwayState(False))
    gun = patterns.ConwayPattern.from_rle("p11dominosparkeron56p27.rle")
    sim.spawn(sim.midpoint - gun.midpoint, gun)
    return sim
