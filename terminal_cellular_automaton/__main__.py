"""Main entrypoint for running a simulation from the command line"""

from .args import parse_args


def main() -> None:
    """Main entrypoint for running an automaton from command line args"""
    result = parse_args()
    result.automaton.start(**result.start_kwargs)


if __name__ == "__main__":
    main()
