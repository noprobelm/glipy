"""A module for storing commonly used scenarios"""

import os
import random
from pathlib import Path

# mypy is unable to find library stubs for this module
import requests  # type: ignore

from . import patterns
from .automaton import Automaton
from .cell import MooreCell
from .coordinate import Coordinate
from .state import ConwayState


def conway_1() -> Automaton:
    """A random game, where each cell has a 1 in 2 chance of spawning as alive"""
    sim = Automaton(MooreCell, ConwayState(False))
    for y in range(sim.ymax + 1):
        for x in range(sim.xmax + 1):
            alive = bool(random.randint(0, 1))
            coord = Coordinate(x, y)
            s = ConwayState(alive)
            sim.set_state(coord, s)
    return sim


def conway_2() -> Automaton:
    """A random game, where each cell has a 1 in 10 chance of spawning as alive"""
    sim = Automaton(MooreCell, ConwayState(False))
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


def pulsar() -> Automaton:
    """A pulsar life generated from the patterns module"""
    sim = Automaton(MooreCell, ConwayState(False))
    pulsar = patterns.Pulsar()
    sim.spawn(sim.midpoint - pulsar.midpoint, pulsar)
    return sim


def glider() -> Automaton:
    """A glider life generated from the patterns module"""
    sim = Automaton(MooreCell, ConwayState(False))
    glider = patterns.Glider()
    sim.spawn(glider.midpoint, glider)
    return sim


def clover_leaf() -> Automaton:
    """A clover leaf generated from the patterns module"""
    sim = Automaton(MooreCell, ConwayState(False))
    leaf = patterns.CloverLeaf()
    sim.spawn(sim.midpoint - leaf.midpoint, leaf)
    return sim


def domino_sparker() -> Automaton:
    """A domino sparker generated from an rle file"""
    sim = Automaton(MooreCell, ConwayState(False))
    rle = os.path.join(
        Path(__file__).parent, "examples/rle/p11dominosparkeron56p27.rle"
    )
    with open(rle, "r") as f:
        lines = f.readlines()
    sparker = patterns.ConwayPattern.from_rle(lines)
    sim.spawn(sim.midpoint - sparker.midpoint, sparker)
    return sim


def from_life(path: str) -> Automaton:
    """Runs a .life from a local path"""
    sim = Automaton(MooreCell, ConwayState(False))
    with open(path, "r") as f:
        lines = f.readlines()
    pattern = patterns.ConwayPattern.from_life(lines)
    sim.spawn(sim.midpoint - pattern.midpoint, pattern)
    return sim


def from_rle(path: str) -> Automaton:
    """Runs a .rle from a local path"""
    sim = Automaton(MooreCell, ConwayState(False))
    with open(path, "r") as f:
        lines = f.readlines()
    pattern = patterns.ConwayPattern.from_rle(lines)
    sim.spawn(sim.midpoint - pattern.midpoint, pattern)
    return sim


def from_url(url: str) -> Automaton:
    """Runs a .rle from a remote URL"""
    sim = Automaton(MooreCell, ConwayState(False))
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error {response.status_code}: {response.reason}")
    data = response.content.decode()
    lines = data.strip().split("\n")
    pattern = patterns.ConwayPattern.from_rle(lines)
    sim.spawn(sim.midpoint - pattern.midpoint, pattern)

    return sim
