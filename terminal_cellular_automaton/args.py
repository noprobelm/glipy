"""Manages command line arguments"""

import argparse

parser = argparse.ArgumentParser(
    description="A pixel physics simulator with terminal rendering"
)

parser.add_argument(
    "-r",
    "--refresh-rate",
    type=int,
    default=60,
    help="The refresh rate of the simulation",
)

parser.add_argument(
    "-d",
    "--duration",
    type=int,
    default=0,
    help="The duration the simulation should run for",
)

parser.add_argument(
    "-x",
    "--debug",
    action="store_true",
    default=False,
    help="Controls if the simluation runs in debug mode",
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
