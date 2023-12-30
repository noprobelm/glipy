"""Main entrypoint for running a simulation"""

from .args import parse_args


def main() -> None:
    """Main entrypoint for running a simulation from command line args"""
    result = parse_args()
    result.automaton.start(**result.start_kwargs)


if __name__ == "__main__":
    main()
