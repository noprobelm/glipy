"""Main entrypoint for running the falling sand simulation"""

from .args import args
from .simulation import Simulation
from . import scenarios


def main() -> None:
    """Main entrypoint for running a simulation on default settings"""
    sim = scenarios.MOORE_NBHD_2
    sim.start(**args)


if __name__ == "__main__":
    main()
