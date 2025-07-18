import math

class Position:
    __slots__ = ['x', 'y', 'z']
    
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def tuple(self, xz=False) -> tuple[float, float, float]:
        if xz:
            return (self.x, self.z)
        return (self.x, self.y, self.z)

    def list(self) -> list[float]:
        return [self.x, self.y, self.z]

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self) -> str:
        return f"Position({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance_to(self, other: 'Position') -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def json(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
        
class BoundingBox:
    __slots__ = ['min_x', 'min_y', 'max_x', 'max_y']
    
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def center(self) -> Position:
        return Position((self.min_x + self.max_x) / 2, (self.min_y + self.max_y) / 2, 0)

    def __str__(self) -> str:
        return f"BoundingBox({self.min_x}, {self.min_y}, {self.max_x}, {self.max_y})"

    def to_start_end(self) -> tuple[Position, Position]:
        return Position(self.min_x, self.min_y, 0), Position(self.max_x, self.max_y, 0)

    def to_start_width_height(self) -> tuple[Position, float, float]:
        return Position(self.min_x, self.min_y, 0), self.max_x - self.min_x, self.max_y - self.min_y

    def __repr__(self) -> str:
        return self.__str__()

    def is_in(self, point: Position, offset: float = 0) -> bool:
        min_x = self.min_x - offset
        max_x = self.max_x + offset
        min_y = self.min_y - offset
        max_y = self.max_y + offset
        return min_x <= point.x <= max_x and min_y <= point.y <= max_y

    def json(self) -> dict:
        return {
            "min_x": self.min_x,
            "min_y": self.min_y,
            "max_x": self.max_x,
            "max_y": self.max_y
        }