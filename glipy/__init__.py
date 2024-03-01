"""Provides convenience functions for building Automatons from various I/O formats"""
import re
from collections import namedtuple
from typing import List, Optional
import random
import requests  # type: ignore

from .coordinate import Coordinate
from .state import ConwayState
from .cell import MooreCell
from .automaton import Automaton

# Stores header data from  properly formatted RLE I/O
RLEHeader = namedtuple(
    "RLEHeader", ["width", "height", "birth_rules", "survival_rules"]
)

# Stores data needed to build a life pattern
PatternData = namedtuple("PatternData", ["states", "xmax", "ymax"])


def from_conway_life(data: str) -> Automaton:
    """Reads lines of a file compliant with life version 1.06

    Args:
        data (str): The life 1.06 data

    Returns:
        PatternData
    """

    data = data.strip()
    lines = data.split("\n")
    xmax = 0
    ymax = 0
    alive = []
    states: List[List[ConwayState]] = []
    for line in lines:
        if line.startswith("#"):
            continue
        split = line.split(" ")
        try:
            coord = Coordinate(int(split[0]), int(split[1]))
        except (ValueError, IndexError):
            raise ValueError(
                f"Malformatted .life file format (see https://conwaylife.com/wiki/Life_1.06)"
            )
        alive.append(coord)
        if coord.x > xmax:
            xmax = coord.x
        if coord.y > ymax:
            ymax = coord.y

    for y in range(ymax + 1):
        states.append([])
        for x in range(xmax + 1):
            if Coordinate(x, y) in alive:
                states[y].append(ConwayState(True))
            else:
                states[y].append(ConwayState(False))

    automaton = Automaton[MooreCell, ConwayState](MooreCell, states, xmax, ymax)

    return automaton


def from_conway_rle(data: str) -> Automaton:
    """Reads lines of a file compliant with Run Length Encoded (RLE)

    Args:
        data (str): The RLE data

    Raises:
        ValueError: A malformatted RLE stream was detected.

    Returns:
        PatternData
    """

    def parse_header(line: str) -> RLEHeader:
        """Parses header data

        Args:
            line (str): The header line from the RLE data

        Raises:
            ValueError: A malformatted RLE stream was detected

        Returns
            RLEHeader
        """
        data = re.search(r"(x = \d+).*(y = \d+)", line)
        if data is None:
            raise ValueError(
                "I/O has malformatted header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
            )

        width_match = re.search(r"\d+", data[1])
        height_match = re.search(r"\d+", data[2])
        if width_match is None or height_match is None:
            raise ValueError(
                "I/O has malformatted header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
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
                raise ValueError(
                    "I/O has malformatted header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
                )

            birth_rules = [int(n) for n in birth_match.group(0)[1:]]
            survival_rules = [int(n) for n in survival_match.group(0)[1:]]

        return RLEHeader(width, height, birth_rules, survival_rules)

    def set_birth_rules(header: RLEHeader):
        """Sets the birth and survival rules (if detected in the header data)

        Args:
            header (RLEHeader): The header data
        """
        ConwayState.birth_rules = header.birth_rules or ConwayState.birth_rules
        ConwayState.survival_rules = header.survival_rules or ConwayState.survival_rules

    def fill_row(row: List[ConwayState], xmax: int) -> List[ConwayState]:
        """Fills in missing values for a row with dead ConwayState cells

        Args:
            row (List[ConwayState]): The row to fill in
            xmax (int): The intended length of the row

        Returns:
            The filled row
        """
        for _ in range(xmax - len(row) + 1):
            row.append(ConwayState(False))

        return row

    def fill_rows(states: List[List[ConwayState]], xmax: int, ymax: int):
        """Fills in the necessary remaining rows with dead ConwayState cells

        Args:
            states (List[List[ConwayState]]): The data to fill
            xmax (int): The intended length of a row
            ymax (int): The intended length of the data

        """
        for _ in range(ymax - len(states) + 1):
            states.append([ConwayState(False) for s in range(xmax + 1)])

        return states

    def parse_states(xmax: int, ymax: int, data: str) -> List[List[ConwayState]]:
        """Parses state data based on RLE I/O stream content

        TODO: This is perfectly functional, but quite messy. We need to come back and do some cleanup

        This function searches for characters and spawns cells based on various criteria defined in the RLE standard.

        - If a row is not filled before reaching a "$" (new row) delimiter, fill it with dead cells
        - If multiple "$" (new row) characters are detected, fill the previous one with dead cells
        - If "!" is detected, fill in the row(s) if they don't meet the RLE header width/height specs
        - If no "!" is detected and we've reached the end, return our state data

        Args:
            xmax (int): The maximum x value of a cell state
            ymax (int): The maximum y value of a cell state
            data (str): Concatenated cell data from the rle file

        Returns:
            A list of conway states resembling a 2d matrix
        """
        nums: List[str] = []
        states: List[List[ConwayState]] = [[]]
        y = 0
        for c in data:
            if c == "!":
                if len(states[y]) < xmax:
                    states[y] = fill_row(states[y], xmax)
                if len(states) < ymax:
                    states = fill_rows(states, xmax, ymax)
                return states

            elif c == "o" or c == "b" or c == "$":
                n = 1 if len(nums) == 0 else int("".join(nums))
                if c == "o" or c == "b":
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
                            [ConwayState(alive=False) for _ in range(xmax + 1)]
                        )
                        y += 1

                    states.append([])
                    y += 1

                nums = []

            elif c.isdigit():
                nums.append(c)

        return states

    lines = data.split("\n")
    for row, line in enumerate(lines):
        if line.strip().startswith("#"):
            continue
        elif "=" in line:
            header = parse_header(line)
            break
    else:
        raise ValueError(
            f"I/O missing header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
        )

    set_birth_rules(header)
    data = "".join(line.strip() for line in lines[row + 1 :])
    states = parse_states(header.width - 1, header.height - 1, data)

    automaton = Automaton[MooreCell, ConwayState](
        MooreCell, states, header.width - 1, header.height - 1
    )

    return automaton


def from_rle_url(url: str) -> Automaton:
    """Runs a .rle from a remote URL"""
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error {response.status_code}: {response.reason}")
    data = response.content.decode()
    automaton = from_conway_rle(data)
    return automaton


def random_conway(xmax: int, ymax: int) -> Automaton:
    automaton = Automaton[MooreCell, ConwayState](
        MooreCell, ConwayState(False), xmax, ymax
    )
    for y in range(automaton.ymax + 1):
        for x in range(automaton.xmax + 1):
            alive = bool(random.randint(0, 1))
            coord = Coordinate(x, y)
            s = ConwayState(alive)
            automaton.set_state(coord, s)
    return automaton
