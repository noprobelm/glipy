"""Manages command line arguments and returns an instance of a Simulator"""

import argparse
import sys
from typing import List, Optional
from collections import namedtuple

from rich.color import ANSI_COLOR_NAMES

from . import scenarios

ArgResult = namedtuple("ArgResult", ["automaton", "start_kwargs"])


def is_hex(h: str) -> bool:
    """Validates a provided hex code

    Args:
        h (str): The hex string to check

    Returns:
        bool: The hex is valid (True) or invalid (False)
    """
    if len(h) > 6:
        return False
    for c in h:
        if not c.isdigit() and not c.isalpha():
            return False
        if c.isalpha() and c.lower() > "f":
            return False

    return True


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
        if c in ANSI_COLOR_NAMES:
            continue
        elif c.startswith("#"):
            if is_hex(c[1:]) is False:
                print(f"Invalid hex code: {c}")
                sys.exit(1)
        else:
            if is_hex(c) is False:
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

    parser.add_argument("target", nargs="?", default="domino_sparker")

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
    if "http" in args["target"]:
        automaton = scenarios.from_url(args["target"])
    elif ".rle" in args["target"]:
        automaton = scenarios.from_rle(args["target"])
    elif ".life" in args["target"]:
        automaton = scenarios.from_life(args["target"])
    else:
        try:
            automaton = getattr(scenarios, args["target"])()
        except AttributeError:
            parser.print_help()
            sys.exit(1)

    if args["colors"] is not None:
        colors = args["colors"].split(" ")
        colors = parse_colors(colors)

        # Pyright doesn't think colors is a valid attr for the CellState protoype. Mypy knows better
        if len(colors) < len(automaton._state_type.colors):  # type: ignore
            args["colors"].extend(automaton._state_type.colors[len(colors) - 1 :])  # type: ignore
        elif len(colors) > len(automaton._state_type.colors):  # type: ignore
            automaton._state_type.colors = colors[: len(automaton._state_type.colors)]  # type: ignore

        else:
            automaton._state_type.colors = colors  # type: ignore

    del args["target"]
    del args["colors"]

    return ArgResult(automaton, args)
