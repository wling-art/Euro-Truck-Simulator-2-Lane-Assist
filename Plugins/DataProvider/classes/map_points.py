from enum import IntEnum
from typing import Literal

class MapColor(IntEnum):
    ROAD = 0
    LIGHT = 1
    DARK = 2
    GREEN = 3

class BaseMapPoint:
    __slots__ = ['x', 'y', 'z', 'neighbors']
    
    x: float
    y: float
    z: float
    neighbors: list[str]


    def __init__(self, x: float, y: float, z: float, neighbors: list[str]):
        self.x = x
        self.y = y
        self.z = z
        self.neighbors = neighbors

    def json(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "neighbors": self.neighbors
        }
        
class RoadMapPoint(BaseMapPoint):
    __slots__ = ['lanes_left', 'lanes_right', 'offset', 'type']
    
    lanes_left: Literal["auto"]
    lanes_right: Literal["auto"]
    offset: float
    type: str

    def __init__(self, x: float, y: float, z: float, neighbors: list[int | str], lanes_left: int | Literal["auto"],
                 lanes_right: int | Literal["auto"], offset: float):
        super().__init__(x, y, z, neighbors)
        self.type = "road"
        self.lanes_left = lanes_left
        self.lanes_right = lanes_right
        self.offset = offset

    def json(self) -> dict:
        return {
            **super().json(),
            "lanes_left": self.lanes_left,
            "lanes_right": self.lanes_right,
            "offset": self.offset
        }


class PolygonMapPoint(BaseMapPoint):
    __slots__ = ['color', 'road_over', 'type']
    
    color: MapColor
    road_over: bool
    type: str

    def __init__(self, x: float, y: float, z: float, neighbors: list[int | str], color: MapColor, road_over: bool):
        super().__init__(x, y, z, neighbors)
        self.type = "polygon"
        self.color = color
        self.road_over = road_over

    def json(self) -> dict:
        return {
            **super().json(),
            "color": self.color,
            "road_over": self.road_over
        }