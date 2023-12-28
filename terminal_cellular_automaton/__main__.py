"""Main entrypoint for running a simulation"""

from . import scenarios
from .args import args


def main() -> None:
    """Main entrypoint for running a simulation on default settings"""
    sim = getattr(scenarios, args["scenario"])()
    del args["scenario"]
    sim.start(**args)


if __name__ == "__main__":
    main()
