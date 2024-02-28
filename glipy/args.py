"""Manages command line arguments and returns an instance of a Simulator"""

import argparse
import sys
from collections import namedtuple
from typing import List, Optional


from . import from_rle_url, from_conway_rle, from_conway_life, random_conway
from .color import Color

ArgResult = namedtuple("ArgResult", ["automaton", "start_kwargs"])


def parse_args(unparsed: Optional[List[str]] = None) -> ArgResult:
    """Parses user args into an automaton and the kwargs necessary to start a simulation.

    Returns:
        ArgResult (namedtuple): Contains the 'automaton' and 'start_kwargs' attrs, which are used to run the sim
    """

    parser = argparse.ArgumentParser(
        description="A cellular automaton simulator with support for terminal rendering"
    )

    parser.add_argument("target", nargs="?", default=None)

    parser.add_argument(
        "-r",
        "--refresh-rate",
        type=int,
        default=30,
        help="The refresh rate of the simulation",
    )

    parser.add_argument(
        "-g",
        "--generations",
        type=int,
        default=0,
        help="The number of generations the simulation should run for",
    )

    parser.add_argument("-c", "--colors", nargs="?")

    parser.add_argument(
        "-x",
        "--debug",
        action="store_true",
        default=False,
        help="Sets the simluation to run in debug mode",
    )

    parser.add_argument(
        "-n",
        "--no-render",
        dest="render",
        action="store_false",
        default=True,
        help="Disables simulation rendering to the terminal",
    )

    args = vars(parser.parse_args(unparsed or sys.argv[1:]))

    if args["target"] is None:
        automaton = random_conway()
    elif "http" in args["target"]:
        automaton = from_rle_url(args["target"])
    elif ".rle" in args["target"]:
        with open(args["target"], "r") as f:
            data = f.read()
        automaton = from_conway_rle(data)
    elif ".life" in args["target"]:
        with open(args["target"], "r") as f:
            data = f.read()
        automaton = from_conway_life(data)

    if args["colors"] is not None:
        colors = [Color(color) for color in args["colors"].split(" ")]
        automaton.colors = colors

    del args["target"]
    del args["colors"]

    return ArgResult(automaton, args)
