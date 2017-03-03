import math

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


class Coord:
    """Represents an (x,y) coordinate on the board."""

    def __init__(self, c):
        self.x = c[0]
        self.y = c[1]

    def up(self):
        """Return up direction."""
        return Coord([self.x, self.y - 1])

    def down(self):
        """Return down direction."""
        return Coord([self.x, self.y + 1])

    def left(self):
        """Return left direction."""
        return Coord([self.x - 1, self.y])

    def right(self):
        """Return up direction."""
        return Coord([self.x + 1, self.y])

    def distance(self, other):
        """Return euclidean distance to another coordinate."""
        d = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return d

    def sub(self, other):
        """Subtract one coordinate from self."""
        return Coord([self.x - other.x, self.y - other.y])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"