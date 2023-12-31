"""Tests various functions within the args module"""

from ward import test
import sys

sys.path.append("../")
from terminal_cellular_automaton import args


@test("is_ansi returns False for invalid ANSI colors")
def _():
    assert args.is_ansi("orange") is False
    assert args.is_ansi("RED") is False


@test("is_ansi returns True for valid ANSI colors")
def _():
    assert args.is_ansi("red") is True


@test("is_hex returns False for strings containing non-alpha or non-digit chars")
def _():
    assert args.is_hex("FF!000") is False


@test("is_hex returns False for strings not exactly 6 chars in length")
def _():
    assert args.is_hex("FF000") is False
    assert args.is_hex("FF00000") is False


@test(
    "is_hex returns False if the provided string contains alpha characters beyond the letter f"
)
def _():
    assert args.is_hex("GG0000") is False


@test("is_hex works with case insensitive strings")
def _():
    assert args.is_hex("ff0000") is True
    assert args.is_hex("FF0000") is True


@test("parse_colors works with a sequence of valid ansi or hex codes")
def _():
    assert args.parse_colors(["red", "000000"]) == ["red", "#000000"]


@test(
    "parse_colors will insert '#' characters at the beginning of valid hex codes if they're missing"
)
def _():
    assert args.parse_colors(["000000"]) == ["#000000"]
