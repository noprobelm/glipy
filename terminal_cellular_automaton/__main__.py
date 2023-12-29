"""Main entrypoint for running a simulation"""

from .args import sim, args


def main() -> None:
    """Main entrypoint for running a simulation from command line args"""
    sim.start(**args)


if __name__ == "__main__":
    main()
