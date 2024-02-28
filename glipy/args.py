"""Manages command line arguments and returns an instance of a Simulator"""

import argparse
import sys
from collections import namedtuple
from typing import List, Optional


from . import from_rle_url, from_conway_rle, from_conway_life, random_conway
from .validators import validate_hex, validate_ansi

ArgResult = namedtuple("ArgResult", ["automaton", "start_kwargs"])


def parse_colors(colors: List[str]) -> List[str]:
    """Parses color names from parsed args

    - If a color is found in the ANSI_COLOR_NAMES constant, move on
    - Otherwise, the color is a hex. Validate it, insert a "#" if necessary

    Args:
        colors (List[str]): The list of colors to parse

    Returns:
        The parsed list of colors
    """

    for i, c in enumerate(colors):
        if validate_ansi(c):
            continue
        if c.startswith("#"):
            if validate_hex(c[1:]) is False:
                print(f"Invalid hex code: {c}")
                sys.exit(1)
        else:
            if validate_hex(c) is False:
                print(f"Invalid hex code: {c}")
                sys.exit(1)
            c = f"#{c}"
        colors[i] = c

    return colors


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
        colors = args["colors"].split(" ")
        colors = parse_colors(colors)
        automaton.colors = colors

    del args["target"]
    del args["colors"]

    return ArgResult(automaton, args)
