class ColorParseError(Exception):
    """The color could not be parsed"""


class Color(str):
    """A string representing a color. Implements validating logic to ensure a valid hex code is used

    Attributes:
        color (str): The color string

    Raises:
        ColorParseError: The color could not be parsed
    """

    def __new__(cls, hex_color):
        """Creates a new instance of the Color class"""

        instance = super().__new__(cls, hex_color)
        return instance

    def __init__(self, hex_color: str):
        """Initializes an instance of the Color class

        Args:
            color (str): The color to initialize
        """
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]
            if len(hex_color) != 6:
                raise ColorParseError(f"Invalid hex: '{hex_color}'")
            for c in hex_color:
                if (not c.isdigit() and not c.isalpha()) or (
                    c.isalpha() and c.lower() > "f"
                ):
                    raise ColorParseError(f"Invalid hex: '{hex_color}'")

        self.color = f"#{hex_color}"

    def __str__(self) -> str:
        return self.color
