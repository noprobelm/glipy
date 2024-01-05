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
    automaton = Automaton[MooreCell, ConwayState](MooreCell, ConwayState(False))
    for y in range(automaton.ymax + 1):
        for x in range(automaton.xmax + 1):
            alive = bool(random.randint(0, 1))
            coord = Coordinate(x, y)
            s = ConwayState(alive)
            automaton.set_state(coord, s)
    return automaton


def conway_2() -> Automaton:
    """A random game, where each cell has a 1 in 10 chance of spawning as alive"""
    automaton = Automaton[MooreCell, ConwayState](MooreCell, ConwayState(False))
    for y in range(automaton.ymax + 1):
        for x in range(automaton.xmax + 1):
            coord = Coordinate(x, y)
            r = random.randint(0, 10)
            if r > 9:
                alive = True
            else:
                alive = False
            s = ConwayState(alive)
            automaton.set_state(coord, s)
    return automaton


def pulsar() -> Automaton:
    """A pulsar life generated from the patterns module"""
    automaton = Automaton[MooreCell, ConwayState](MooreCell, ConwayState(False))
    pulsar = patterns.Pulsar()
    automaton.spawn(automaton.midpoint - pulsar.midpoint, pulsar)
    return automaton


def glider() -> Automaton:
    """A glider life generated from the patterns module"""
    automaton = Automaton[MooreCell, ConwayState](MooreCell, ConwayState(False))
    glider = patterns.Glider()
    automaton.spawn(glider.midpoint, glider)
    return automaton


def clover_leaf() -> Automaton:
    """A clover leaf generated from the patterns module"""
    automaton = Automaton[MooreCell, ConwayState](MooreCell, ConwayState(False))
    leaf = patterns.CloverLeaf()
    automaton.spawn(automaton.midpoint - leaf.midpoint, leaf)
    return automaton


def domino_sparker() -> Automaton:
    """A domino sparker generated from an rle file"""
    automaton = Automaton[MooreCell, ConwayState](MooreCell, ConwayState(False))
    rle = os.path.join(Path(__file__).parent, "data/rle/p11dominosparkeron56p27.rle")
    sparker = patterns.ConwayPattern.from_rle(path)
    automaton.spawn(automaton.midpoint - sparker.midpoint, sparker)
    return automaton


def from_life(path: str) -> Automaton:
    """Runs a .life from a local path"""
    automaton = Automaton[MooreCell, ConwayState](MooreCell, ConwayState(False))
    pattern = patterns.ConwayPattern.from_life(path)
    automaton.spawn(automaton.midpoint - pattern.midpoint, pattern)
    return automaton


def from_rle(path: str) -> Automaton:
    """Runs a .rle from a local path"""
    automaton = Automaton[MooreCell, ConwayState](MooreCell, ConwayState(False))
    pattern = patterns.ConwayPattern.from_rle(path)
    automaton.spawn(automaton.midpoint - pattern.midpoint, pattern)
    return automaton


def from_url(url: str) -> Automaton:
    """Runs a .rle from a remote URL"""
    automaton = Automaton[MooreCell, ConwayState](MooreCell, ConwayState(False))
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error {response.status_code}: {response.reason}")
    data = response.content.decode()
    lines = data.strip().split("\n")
    pattern = patterns.ConwayPattern.from_rle(lines)
    automaton.spawn(automaton.midpoint - pattern.midpoint, pattern)

    return automaton
