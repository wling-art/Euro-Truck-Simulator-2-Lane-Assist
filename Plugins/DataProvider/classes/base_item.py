from enum import IntEnum

class ItemType(IntEnum):
    Terrain = 1
    Building = 2
    Road = 3
    Prefab = 4
    Model = 5
    Company = 6
    Service = 7
    CutPlane = 8
    Mover = 9
    NoWeather = 11
    City = 12
    Hinge = 13
    MapOverlay = 18
    Ferry = 19
    Sound = 21
    Garage = 22
    CameraPoint = 23
    Trigger = 34
    FuelPump = 35  # services
    Sign = 36  # sign
    BusStop = 37
    TrafficRule = 38  # traffic_area
    BezierPatch = 39
    Compound = 40
    TrajectoryItem = 41
    MapArea = 42
    FarModel = 43
    Curve = 44
    CameraPath = 45
    Cutscene = 46
    Hookup = 47
    VisibilityArea = 48
    Gate = 49

class BaseItem:
    __slots__ = ['uid', 'type', 'x', 'y', 'sector_x', 'sector_y']
    
    uid: str
    type: ItemType
    x: float
    y: float

    def __init__(self, uid: int | str, type: ItemType, x: float, y: float):
        self.uid = uid
        self.type = type
        self.x = x
        self.y = y

    def json(self) -> dict:
        return {
            "uid": self.uid,
            "type": self.type,
            "x": self.x,
            "y": self.y,
        }