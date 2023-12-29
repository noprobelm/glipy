"""Manages command line arguments and returns an instance of a Simulator"""

import argparse
from . import scenarios
import sys

parser = argparse.ArgumentParser(
    description="A cellular automaton simulator with support for terminal rendering"
)

parser.add_argument("target")

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

args = vars(parser.parse_args())
if "http" in args["target"]:
    sim = scenarios.from_url(args["target"])
elif ".rle" in args["target"]:
    sim = scenarios.from_rle(args["target"])
elif ".life" in args["target"]:
    sim = scenarios.from_life(args["target"])
else:
    try:
        sim = getattr(scenarios, args["target"])()
    except AttributeError:
        parser.print_help()
        sys.exit(1)

del args["target"]
