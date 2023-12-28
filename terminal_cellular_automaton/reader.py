from collections import namedtuple
import re
from typing import List
from .state import ConwayState
from .coordinate import Coordinate

Header = namedtuple("Header", ["width", "height", "birth_rules", "survival_rules"])
PatternData = namedtuple("PatternData", ["xmax", "ymax", "states"])


def life(path: str) -> PatternData:
    with open(path, "r") as f:
        lines = f.readlines()

    xmax = 0
    ymax = 0
    alive = []
    states: List[List[ConwayState]] = []
    for line in lines:
        if line.startswith("#"):
            continue
        split = line.split(" ")
        coord = Coordinate(int(split[0]), int(split[1]))
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

    return PatternData(xmax, ymax, states)


def rle(path: str) -> PatternData:
    def parse_header(line: str) -> Header:
        data = re.search(r"(x = \d+).*(y = \d+)", line)
        if data is None:
            raise ValueError(
                f"File {path} has malformatted header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
            )

        width_match = re.search(r"\d+", data[1])
        height_match = re.search(r"\d+", data[2])
        if width_match is None or height_match is None:
            raise ValueError(
                f"File {path} has malformatted header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
            )
        width = int(width_match.group(0))
        height = int(height_match.group(0))

        rules = re.search(r"rule = .*", line)
        if rules is None:
            birth_rules = None
            survival_rules = None
        else:
            birth_match = re.search(r"B\d+", line)
            survival_match = re.search(r"S\d+", line)
            if birth_match is None or survival_match is None:
                raise ValueError(
                    f"File {path} has malformatted header line (see https://conwaylife.com/wiki/Run_Length_Encoded)"
                )

            birth_rules = [int(n) for n in birth_match.group(0)[1:]]
            survival_rules = [int(n) for n in survival_match.group(0)[1:]]

        return Header(width, height, birth_rules, survival_rules)

    def set_birth_rules(header: Header):
        ConwayState.birth_rules = header.birth_rules or ConwayState.birth_rules
        ConwayState.survival_rules = header.survival_rules or ConwayState.survival_rules

    def parse_states(xmax: int, ymax: int, data: str) -> List[List[ConwayState]]:
        nums: List[str] = []
        states: List[List[ConwayState]] = [[]]
        y = 0
        for c in data:
            if c == "!":
                if len(states[y]) < xmax:
                    for _ in range(xmax - len(states[y]) + 1):
                        states[y].append(ConwayState(alive=False))
                if len(states) < ymax:
                    for _ in range(ymax - len(states) + 1):
                        states.append([ConwayState(False) for s in range(xmax + 1)])
                return states
            elif c == "o" or c == "b":
                if len(nums) == 0:
                    n = 1
                else:
                    n = int("".join(nums))

                for _ in range(n):
                    if c == "o":
                        states[y].append(ConwayState(alive=True))
                    else:
                        states[y].append(ConwayState(alive=False))

                nums = []
            elif c == "$":
                if len(states[y]) <= xmax:
                    for _ in range(xmax - len(states[y]) + 1):
                        states[y].append(ConwayState(alive=False))

                if len(nums) == 0:
                    n = 1
                else:
                    n = int("".join(nums))
                if n > 0:
                    for _ in range(n - 1):
                        states.append(
                            [ConwayState(alive=False) for _ in range(xmax + 1)]
                        )
                        y += 1
                    else:
                        states.append([])
                        y += 1

                nums = []

            elif c.isdigit():
                nums.append(c)

        return states

    with open(path, "r") as f:
        lines = f.readlines()

    header = None
    row = None
    for row, line in enumerate(lines):
        if line.strip().startswith("#"):
            continue
        if "=" in line:
            header = parse_header(line)
            break
    if header is None or row is None:
        raise ValueError(
            f"No valid RLE header found in file '{path}'. See formatting standards at https://conwaylife.com/wiki/Run_Length_Encoded"
        )

    set_birth_rules(header)
    data = "".join(line.strip() for line in lines[row + 1 :])
    states = parse_states(header.width - 1, header.height - 1, data)
    return PatternData(header.width - 1, header.height - 1, states)
