"""Tests various functions within the args module"""

from ward import test, raises
from glipy.color import Color, ColorParseError


@test("Color raises 'ColorParseError' if an invalid hex is passed")
def _():
    with raises(ColorParseError):
        Color("FF!000")
        Color("FF000")
        Color("FF00000")
        Color("GG0000")


@test("Color is case insensitive")
def _():
    assert Color("ff0000") == "#ff0000"
    assert Color("FF0000") == "#FF0000"
