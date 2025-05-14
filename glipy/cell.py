from typing import Protocol

from .coordinate import Coordinate


class Cell(Protocol):
    """A protocol to reference when creating a new type of cell.

    A cell is primarily defined by its neighbors. A class that conforms to this protocol shoud have an __init__ method
    which accepts a coordinate, and a get_neighbors method that will retreive valid neighbors based on a maximum
    possible coordinate

    Attributes:
        coord (Coordinate): The coordinate of a given cell
        neighbors (Tuple[Coordinate, ...]): All valid neighbors of a cell based on the coordinate attribute

    """

    coord: Coordinate
    neighbors: tuple[Coordinate, ...]

    def __init__(self, coord: Coordinate) -> None:
        """Initializes an instance of a cell. The coord attr should be set here."""

    def get_neighbors(self, max_coord: Coordinate) -> list[Coordinate]:
        """Accesses members of a cell's neighborhood and returns a list of valid neighbors.

        This is usually achieved by checking coordinates against a maximum possible coordinate. The
        Coordinate.__contains__ special method is available for determining neighbors.

        Args:
            max_coord (Coordinate): The maximum possible coordinate of a neighbor (usually the max coord of the
                underlying matrix)

        Returns:
            A list of all valid neighbors

        """


class MooreCell:
    """A cell that references members of a MooreNeighborhood.

    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | C | 5 |
    +---+---+---+
    | 6 | 7 | 8 |
    +---+---+---+

    """

    neighbors: tuple[Coordinate, ...] = (
        # Upper left
        Coordinate(-1, -1),
        # Upper
        Coordinate(0, -1),
        # Upper right
        Coordinate(1, -1),
        # Right
        Coordinate(1, 0),
        # Lower right
        Coordinate(1, 1),
        # Lower
        Coordinate(0, 1),
        # Lower left
        Coordinate(-1, 1),
        # Left
        Coordinate(-1, 0),
    )

    def __init__(self, coord: Coordinate) -> None:
        """Initializes an instance of the MooreCell class."""
        self.coord = coord

    def get_neighbors(self, max_coord: Coordinate) -> list[Coordinate]:
        """Gets neighbors based on the max coord.

        Neighbors will usually be the eight surrounding cells in an automaton, but for cells living along the min/max
        coords, neighbors will wrap around to the other side of this grid. This ensures continuity and enables
        a life to wrap around the other side of the simulation once it reaches a boundary, emulating a pseudo-infinite
        space.

        Args:
            max_coord (Coordinate): The maximum coordinate found in the underlying Automaton

        Returns:
            A list of the cell's neighbors

        """
        neighbors = []
        for nc in self.neighbors:
            n = nc + self.coord
            if n.x < 0 and n.y < 0:
                n = Coordinate(max_coord.x, max_coord.y)
            elif n.x > max_coord.x and n.y > max_coord.y:
                n = Coordinate(0, 0)
            elif n.x < 0 and n.y > max_coord.y:
                n = Coordinate(max_coord.x, 0)
            elif n.y < 0 and n.x > max_coord.x:
                n = Coordinate(0, max_coord.y)
            elif n.x > max_coord.x:
                n = Coordinate(0, n.y)
            elif n.y < 0:
                n = Coordinate(n.x, max_coord.y)
            elif n.y > max_coord.y:
                n = Coordinate(n.x, 0)
            elif n.x < 0:
                n = Coordinate(max_coord.x, n.y)
            elif n.x > max_coord.x:
                n = Coordinate(0, n.y)

            neighbors.append(n)

        return neighbors


class NeumannCell:
    """A cell that references members of a Von Neumann neighborhood.

        +---+
        | 2 |
    +---+---+---+
    | 4 | C | 5 |
    +---+---+---+
        | 7 |
        +---+
    """

    neighbors: tuple[Coordinate, ...] = (
        # Upper
        Coordinate(0, -1),
        # Right
        Coordinate(1, 0),
        # Lower
        Coordinate(0, 1),
        # Left
        Coordinate(-1, 0),
    )

    def __init__(self, coord: Coordinate) -> None:
        """Initializes an instance of the MooreCell class."""
        self.coord = coord

    def get_neighbors(self, max_coord: Coordinate) -> list[Coordinate]:
        """Gets neighbors based on the max coord.

        Neighbors will usually be the eight surrounding cells in an automaton, but for cells living along the min/max
        coords, neighbors will wrap around to the other side of this grid. This ensures continuity and enables
        a life to wrap around the other side of the simulation once it reaches a boundary, emulating a pseudo-infinite
        space.

        Args:
            max_coord (Coordinate): The maximum coordinate found in the underlying Automaton

        Returns:
            A list of the cell's neighbors

        """
        neighbors = []
        for nc in self.neighbors:
            n = nc + self.coord
            if n.x < 0 and n.y < 0:
                n = Coordinate(max_coord.x, max_coord.y)
            elif n.x > max_coord.x and n.y > max_coord.y:
                n = Coordinate(0, 0)
            elif n.x < 0 and n.y > max_coord.y:
                n = Coordinate(max_coord.x, 0)
            elif n.y < 0 and n.x > max_coord.x:
                n = Coordinate(0, max_coord.y)
            elif n.x > max_coord.x:
                n = Coordinate(0, n.y)
            elif n.y < 0:
                n = Coordinate(n.x, max_coord.y)
            elif n.y > max_coord.y:
                n = Coordinate(n.x, 0)
            elif n.x < 0:
                n = Coordinate(max_coord.x, n.y)
            elif n.x > max_coord.x:
                n = Coordinate(0, n.y)

            neighbors.append(n)

        return neighbors
