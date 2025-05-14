"""This module contains the Color class, which is a string representing valid hex colors."""


class ColorParseError(Exception):
    """The color could not be parsed."""


class Color(str):
    """A string representing a color. Implements validating logic to ensure a valid hex code is used.

    Attributes:
        color (str): The color string

    Raises:
        ColorParseError: The color could not be parsed

    """

    def __new__(cls, hex_color):
        """Creates a new instance of the Color class."""
        hex_color = hex_color.removeprefix("#")

        if len(hex_color) != 6:
            msg = f"Invalid hex: '{hex_color}'"
            raise ColorParseError(msg)
        for char in hex_color:
            if (not char.isdigit() and not char.isalpha()) or (
                char.isalpha() and char.lower() > "f"
            ):
                msg = f"Invalid hex: '{hex_color}'"
                raise ColorParseError(msg)

        hex_color = f"#{hex_color}"
        return super().__new__(cls, hex_color)
