"""Tests CellState behavior"""

from ward import test

from glipy.state import ConwayState


@test("ConwayState: A dead cell next to exactly 3 live cells will resurrect")
def _():
    s = ConwayState(alive=False)
    assert (
        s.change_state([ConwayState(alive=True), ConwayState(alive=True), ConwayState(alive=True)]).alive
        == True
    )


@test(
    "ConwayState: A dead cell next to any number of live cells other than 3 will remain dead",
)
def _():
    s = ConwayState(alive=False)
    assert s.change_state([ConwayState(alive=True), ConwayState(alive=True)]).alive == False


@test("ConwayState: A live cell next to exactly 2 or 3 live cells will remain alive")
def _():
    s = ConwayState(alive=True)
    assert (
        s.change_state([ConwayState(alive=True), ConwayState(alive=True), ConwayState(alive=True)]).alive
        == True
    )
    assert s.change_state([ConwayState(alive=True), ConwayState(alive=True)]).alive == True


@test(
    "ConwayState: A live cell next to any number of cells other than 2 or 3 live cells will die",
)
def _():
    s = ConwayState(alive=True)
    assert s.change_state([ConwayState(alive=True)]).alive == False


@test(
    "ConwayState: A live cell's color will correspond to the first color in the 'colors' attribute",
)
def _():
    s = ConwayState(alive=True)
    assert s.color == s.colors[0]


@test(
    "ConwayState: A dead cell's color will correspond to the second color in the 'colors' attribute",
)
def _():
    s = ConwayState(alive=False)
    assert s.color == s.colors[1]


@test(
    "Colors Interface: The default colors of a CellState will be overriden when new colors are provided to the setter",
)
def _():
    s = ConwayState(alive=True)
    colors = ["blue", "yellow"]
    ConwayState.set_colors(colors)
    assert s.colors == colors
    assert len(s.colors) == 2


@test(
    "Colors Interface: Providing fewer colors than the number of states will result in a CellState right padding with \
    existing colors",
)
def _():
    s = ConwayState(alive=True)
    old = s.colors
    colors = ["blue"]
    ConwayState.set_colors(colors)
    assert s.colors == ["blue", old[1]]


@test(
    "Colors Interface: Providing more colors than the number of states will result in a the extra colors being dropped",
)
def _():
    s = ConwayState(alive=True)
    colors = ["blue", "green", "yellow"]
    ConwayState.set_colors(colors)
    assert s.colors == ["blue", "green"]
