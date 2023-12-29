"""Manages command line arguments and returns an instance of a Simulator"""

import argparse
from . import scenarios
import sys

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

parser.add_argument("-c", "--colors", nargs="+")

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

if args["colors"] is not None:
    if len(args["colors"]) < len(sim._state_type.colors):  # type: ignore
        args["colors"].extend(sim._state_type.colors[len(args["colors"]) - 1 :])  # type: ignore
    elif len(args["colors"]) > len(sim._state_type.colors):  # type: ignore
        sim._state_type.colors = args["colors"][: len(sim._state_type.colors)]  # type: ignore
    sim._state_type.colors = args["colors"]  # type: ignore

del args["target"]
del args["colors"]
