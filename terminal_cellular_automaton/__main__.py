"""Main entrypoint for running the falling sand simulation"""

from . import scenarios
from .args import args


def main() -> None:
    """Main entrypoint for running a simulation on default settings"""
    sim = scenarios.CONWAY_2
    sim.start(**args)


if __name__ == "__main__":
    main()
