"""Provides convenience functions for building Automatons from various I/O formats."""

import random
import re
from typing import NamedTuple

import requests

from .automaton import Automaton
from .cell import Cell, MooreCell
from .coordinate import Coordinate
from .state import ConwayState

HTTP_OK = 200

# Stores header data from  properly formatted RLE I/O
RLEHeader = NamedTuple(
    "RLEHeader",
    ["width", "height", "birth_rules", "survival_rules"],
)

# Stores data needed to build a life pattern
PatternData = NamedTuple("PatternData", ["states", "xmax", "ymax"])


def from_conway_life(data: str, cell_type: type[Cell] = MooreCell) -> Automaton:
    """Read lines of a file compliant with life version 1.06.

    Args:
        data (str): The life 1.06 data
        cell_type (type[Cell]): The cell type to use for this automoaton.

    Returns:
        PatternData

    """
    data = data.strip()
    lines = data.split("\n")
    xmax = 0
    ymax = 0
    alive = []
    states: list[list[ConwayState]] = []
    for line in lines:
        if line.startswith("#"):
            continue
        split = line.split(" ")
        try:
            coord = Coordinate(int(split[0]), int(split[1]))
        except (ValueError, IndexError):
            msg = "Malformatted .life file format (see https://conwaylife.com/wiki/Life_1.06)"
            raise ValueError(
                msg,
            ) from ValueError
        alive.append(coord)
        xmax = max(xmax, coord.x)
        ymax = max(ymax, coord.y)

    for y in range(ymax + 1):
        states.append([])
        for x in range(xmax + 1):
            if Coordinate(x, y) in alive:
                states[y].append(ConwayState(alive=True))
            else:
                states[y].append(ConwayState(alive=False))

    automaton: Automaton = Automaton(cell_type, states, xmax, ymax)

    return automaton


def from_conway_rle(data: str, cell_type: type[Cell] = MooreCell) -> Automaton:
    """Read lines of a file compliant with Run Length Encoded (RLE).

    Args:
        data (str): The RLE data
        cell_type (type[Cell]): The cell type to use for this automaton.

    Raises:
        ValueError: A malformatted RLE stream was detected.

    Returns:
        PatternData

    """

    def parse_header(line: str) -> RLEHeader:
        """Parse header data.

        Args:
            line (str): The header line from the RLE data

        Raises:
            ValueError: A malformatted RLE stream was detected

        Returns:
            RLEHeader

        """
        data = re.search(r"(x = \d+).*(y = \d+)", line)
        if data is None:
            msg = "I/O has malformatted header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
            raise ValueError(
                msg,
            )

        width_match = re.search(r"\d+", data[1])
        height_match = re.search(r"\d+", data[2])
        if width_match is None or height_match is None:
            msg = "I/O has malformatted header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
            raise ValueError(
                msg,
            )
        width = int(width_match.group(0))
        height = int(height_match.group(0))

        rules = re.search(r"rule = .*", line)
        if rules is None:
            birth_rules = None
            survival_rules = None
        else:
            birth_match = re.search(r"[bB]\d+", line)
            survival_match = re.search(r"[sS]\d+", line)
            if birth_match is None or survival_match is None:
                msg = "I/O has malformatted header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
                raise ValueError(
                    msg,
                )

            birth_rules = [int(n) for n in birth_match.group(0)[1:]]
            survival_rules = [int(n) for n in survival_match.group(0)[1:]]

        return RLEHeader(width, height, birth_rules, survival_rules)

    def set_birth_rules(header: RLEHeader) -> None:
        """Set the birth and survival rules (if detected in the header data).

        Args:
            header (RLEHeader): The header data

        """
        ConwayState.birth_rules = header.birth_rules or ConwayState.birth_rules
        ConwayState.survival_rules = header.survival_rules or ConwayState.survival_rules

    def fill_row(row: list[ConwayState], xmax: int) -> list[ConwayState]:
        """Fill in missing values for a row with dead ConwayState cells.

        Args:
            row (List[ConwayState]): The row to fill in
            xmax (int): The intended length of the row

        Returns:
            The filled row

        """
        row.extend(ConwayState(alive=False) for _ in range(xmax - len(row) + 1))

        return row

    def fill_rows(
        states: list[list[ConwayState]],
        xmax: int,
        ymax: int,
    ) -> list[list[ConwayState]]:
        """Fill in the necessary remaining rows with dead ConwayState cells.

        Args:
            states (List[List[ConwayState]]): The data to fill
            xmax (int): The intended length of a row
            ymax (int): The intended length of the data

        """
        states.extend(
            [
                [ConwayState(alive=False) for _ in range(xmax + 1)]
                for _ in range(ymax - len(states) + 1)
            ],
        )

        return states

    def parse_states(xmax: int, ymax: int, data: str) -> list[list[ConwayState]]:
        """Parse state data based on RLE I/O stream content.

        TODO: This is perfectly functional, but quite messy. We need to come back and do some
        cleanup

        This function searches for characters and spawns cells based on various criteria defined in
        the RLE standard.

        - If a row is not filled before reaching a "$" (new row) delimiter, fill it with dead cells
        - If multiple "$" (new row) characters are detected, fill the previous one with dead cells
        - If "!" is detected, fill in the row(s) if they don't meet the RLE header width/height
          specs
        - If no "!" is detected and we've reached the end, return our state data

        Args:
            xmax (int): The maximum x value of a cell state
            ymax (int): The maximum y value of a cell state
            data (str): Concatenated cell data from the rle file

        Returns:
            A list of conway states resembling a 2d matrix

        """
        nums: list[str] = []
        states: list[list[ConwayState]] = [[]]
        y = 0
        for c in data:
            if c == "!":
                if len(states[y]) < xmax:
                    states[y] = fill_row(states[y], xmax)
                if len(states) < ymax:
                    states = fill_rows(states, xmax, ymax)
                return states

            if c in {"o", "b", "$"}:
                n = 1 if len(nums) == 0 else int("".join(nums))
                if c in {"o", "b"}:
                    for _ in range(n):
                        if c == "o":
                            states[y].append(ConwayState(alive=True))
                        else:
                            states[y].append(ConwayState(alive=False))
                else:
                    if len(states[y]) <= xmax:
                        states[y] = fill_row(states[y], xmax)

                    for _ in range(n - 1):
                        states.append(
                            [ConwayState(alive=False) for _ in range(xmax + 1)],
                        )
                        y += 1

                    states.append([])
                    y += 1

                nums = []

            elif c.isdigit():
                nums.append(c)

        return states

    lines = data.split("\n")
    for _row, line in enumerate(lines):
        if line.strip().startswith("#"):
            continue
        if "=" in line:
            header = parse_header(line)
            break
    else:
        msg = "I/O missing header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
        raise ValueError(
            msg,
        )

    set_birth_rules(header)
    data = "".join(line.strip() for line in lines[_row + 1 :])
    states = parse_states(header.width - 1, header.height - 1, data)

    automaton: Automaton = Automaton(
        cell_type,
        states,
        header.width - 1,
        header.height - 1,
    )

    return automaton


def from_rle_url(url: str, cell_type: type[Cell] = MooreCell) -> Automaton:
    """Run a .rle from a remote URL."""
    response = requests.get(url, timeout=5)
    if response.status_code != HTTP_OK:
        msg = f"Error {response.status_code}: {response.reason}"
        raise ValueError(msg)
    data = response.content.decode()
    automaton: Automaton = from_conway_rle(data, cell_type)
    return automaton


def random_conway(xmax: int, ymax: int, cell_type: type[Cell] = MooreCell) -> Automaton:
    """Generate a random conway automaton."""
    automaton: Automaton = Automaton(cell_type, ConwayState(alive=False), xmax, ymax)
    for y in range(automaton.ymax + 1):
        for x in range(automaton.xmax + 1):
            alive = bool(random.randint(0, 1))
            coord = Coordinate(x, y)
            s = ConwayState(alive)
            automaton.set_state(coord, s)
    return automaton
