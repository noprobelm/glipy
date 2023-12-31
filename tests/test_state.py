"""Tests CellState behavior"""

from ward import test, fixture
import sys

sys.path.append("../")
from terminal_cellular_automaton.cell import MooreCell
from terminal_cellular_automaton.state import ConwayState
from terminal_cellular_automaton.coordinate import Coordinate


@test("ConwayState: A dead cell next to exactly 3 live cells will resurrect")
def _():
    s = ConwayState(False)
    assert (
        s.change_state([ConwayState(True), ConwayState(True), ConwayState(True)]).alive
        == True
    )


@test(
    "ConwayState: A dead cell next to any number of live cells other than 3 will remain dead"
)
def _():
    s = ConwayState(False)
    assert s.change_state([ConwayState(True), ConwayState(True)]).alive == False


@test("ConwayState: A live cell next to exactly 2 or 3 live cells will remain alive")
def _():
    s = ConwayState(True)
    assert (
        s.change_state([ConwayState(True), ConwayState(True), ConwayState(True)]).alive
        == True
    )
    assert s.change_state([ConwayState(True), ConwayState(True)]).alive == True


@test(
    "ConwayState: A live cell next to any number of cells other than 2 or 3 live cells will die"
)
def _():
    s = ConwayState(True)
    assert s.change_state([ConwayState(True)]).alive == False


@test(
    "ConwayState: A live cell's color will correspond to the first color in the 'colors' attribute"
)
def _():
    s = ConwayState(True)
    assert s.color == s.colors[0]


@test(
    "ConwayState: A dead cell's color will correspond to the second color in the 'colors' attribute"
)
def _():
    s = ConwayState(False)
    assert s.color == s.colors[1]
