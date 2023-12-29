"""Main entrypoint for running a simulation"""

from . import scenarios
from .args import args


def main() -> None:
    """Main entrypoint for running a simulation from command line args"""
    if all(a == None for a in [args["scenario"], args["rle"], args["url"]]):
        sim = scenarios.pulsar()

    elif args["rle"]:
        sim = scenarios.from_rle(args["rle"])

    elif args["url"]:
        sim = scenarios.from_url(args["url"])

    else:
        sim = getattr(scenarios, args["scenario"])()

    del args["scenario"]
    del args["rle"]
    del args["url"]

    sim.start(**args)


if __name__ == "__main__":
    main()
