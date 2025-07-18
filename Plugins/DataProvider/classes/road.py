import math
from Plugins.DataProvider.classes.general import Position, BoundingBox
from Plugins.DataProvider.classes.base_item import BaseItem, ItemType

class RoadLook:
    __slots__ = ['token', 'name', 'lanes_left', 'lanes_right', 'offset', 'shoulder_space_left', 'shoulder_space_right']
    
    token: str
    name: str
    lanes_left: list[str]
    lanes_right: list[str]
    offset: float
    shoulder_space_left: float
    shoulder_space_right: float

    def __init__(self, token: str, name: str, lanes_left: list[str], lanes_right: list[str], offset: float | None,
                 shoulder_space_left: float | None, shoulder_space_right: float | None):
        self.token = token
        self.name = name
        self.lanes_left = lanes_left
        self.lanes_right = lanes_right
        self.offset = offset
        self.shoulder_space_left = shoulder_space_left
        self.shoulder_space_right = shoulder_space_right

    def json(self) -> dict:
        return {
            "token": self.token,
            "name": self.name,
            "lanes_left": self.lanes_left,
            "lanes_right": self.lanes_right,
            "offset": self.offset,
            "shoulder_space_left": self.shoulder_space_left,
            "shoulder_space_right": self.shoulder_space_right
        }
        
    def __str__(self) -> str:
        return f"RoadLook({self.token}, {self.name}, {self.lanes_left}, {self.lanes_right}, {self.offset}, {self.shoulder_space_left}, {self.shoulder_space_right})"
    
    def __repr__(self) -> str:
        return self.__str__()

class Railing:
    __slots__ = ["right_railing", "right_railing_offset", "left_railing", "left_railing_offset"]
    
    right_railing: str
    right_railing_offset: int
    left_railing: str
    left_railing_offset: int
    
    def __init__(self, right_railing: str, right_railing_offset: int, left_railing: str, left_railing_offset: int):
        self.right_railing = right_railing
        self.right_railing_offset = right_railing_offset
        self.left_railing = left_railing
        self.left_railing_offset = left_railing_offset
        
    def json(self) -> dict:
        return {
            "right_railing": self.right_railing,
            "right_railing_offset": self.right_railing_offset,
            "left_railing": self.left_railing,
            "left_railing_offset": self.left_railing_offset
        }
        
class Road(BaseItem):
    __slots__ = ['hidden', 'road_look_token', 'start_node_uid', 'end_node_uid', 'length', 'maybe_divided',
                 'type', 'road_look', '_bounding_box', '_lanes', '_points', 'start_node', 'end_node', 'railings']
    
    hidden: bool
    road_look_token: str
    start_node_uid: str
    end_node_uid: str
    length: float
    maybe_divided: bool
    type: ItemType
    road_look: RoadLook
    railings: list[Railing] | None

    # _bounding_box: BoundingBox
    # _lanes: list[Lane]
    # _points: list[Position]

    def __init__(self, uid: int | str, x: float, y: float,
                 hidden: bool | None, road_look_token: str, start_node_uid: str, end_node_uid: str,
                 length: float, maybe_divided: bool | None, railings: list[Railing] | None = None):
        super().__init__(uid, ItemType.Road, x, y)

        self.type = ItemType.Road
        self.hidden = bool(hidden) if hidden is not None else False
        self.road_look_token = road_look_token
        self.start_node_uid = start_node_uid
        self.end_node_uid = end_node_uid
        self.length = length
        self.maybe_divided = maybe_divided
        self.railings = railings if railings is not None else []
        
        self.road_look = None
        self.clear_data()

    def clear_data(self):
        self._lanes = []
        self._bounding_box = None
        self._points = None
        self.start_node = None
        self.end_node = None

    # def get_nodes(self, map=None):
    #     """Populate start_node and end_node if not already set."""
    #     if map is None:
    #         map = data.map
    #         
    #     try:
    #         if not hasattr(self, 'start_node_uid') or not hasattr(self, 'end_node_uid'):
    #             logging.error(f"Road {self.uid} missing node UIDs")
    #             return None, None
# 
    #         if self.start_node is None:
    #             self.start_node = map.get_node_by_uid(self.start_node_uid)
    #         if self.end_node is None:
    #             self.end_node = map.get_node_by_uid(self.end_node_uid)
# 
    #         if self.start_node is None or self.end_node is None:
    #             logging.error(f"Road {self.uid} failed to get nodes")
    #             return None, None
# 
    #         return self.start_node, self.end_node
    #     except Exception as e:
    #         logging.error(f"Error getting nodes for road {self.uid}: {e}")
    #         return None, None

    # def generate_points(self, road_quality: float = 0.5, min_quality: int = 4) -> list[Position]:
    #     try:
    #         start_node, end_node = self.get_nodes()
    #         if not start_node or not end_node:
    #             logging.error(f"Failed to get nodes for road {self.uid}")
    #             return []
    # 
    #         new_points = []
    # 
    #         start_pos = (start_node.x, start_node.z, start_node.y)
    #         end_pos = (end_node.x, end_node.z, end_node.y)
# 
    #         start_quaternion = start_node.rotationQuat if hasattr(start_node, 'rotationQuat') else (0, 0, 0, 0)
    #         end_quaternion = end_node.rotationQuat if hasattr(end_node, 'rotationQuat') else (0, 0, 0, 0)
# 
    #         length = math.sqrt(sum((e - s) ** 2 for s, e in zip(start_pos, end_pos)))
    #         needed_points = max(int(length * road_quality), min_quality)
    # 
    #         for i in range(needed_points):
    #             s = i / (needed_points - 1)
    #             x, y, z = math_helpers.Hermite3D(s, start_pos, end_pos, start_quaternion, end_quaternion, self.length)
    #             new_points.append(Position(x, y, z))
    # 
    #         return new_points
    #     except Exception as e:
    #         logging.exception(f"Error generating points for road {self.uid}: {e}")
    #         return []

    # @property
    # def points(self) -> list[Position]:
    #     if self._points is None:
    #         self._points = self.generate_points()
    #         data.heavy_calculations_this_frame += 1
# 
    #     return self._points
# 
    # @points.setter
    # def points(self, value: list[Position]):
    #     self._points = value

    # @property
    # def lanes(self) -> list[Lane]:
    #     if self._lanes == []:
    #         self._lanes, self._bounding_box = road_helpers.GetRoadLanes(self, data)
    #         data.heavy_calculations_this_frame += 1
    #         data.data_needs_update = True
# 
    #     return self._lanes
# 
    # @lanes.setter
    # def lanes(self, value: list[Lane]):
    #     self._lanes = value
# 
    # @property
    # def bounding_box(self) -> BoundingBox:
    #     if self._bounding_box is None:
    #         if data.heavy_calculations_this_frame >= data.allowed_heavy_calculations:
    #             return BoundingBox(0, 0, 0, 0)
    #         self._lanes, self._bounding_box = road_helpers.GetRoadLanes(self, data)
    #         data.heavy_calculations_this_frame += 1
    #         data.data_needs_update = True
# 
    #     return self._bounding_box
# 
    # @bounding_box.setter
    # def bounding_box(self, value: BoundingBox):
    #     self._bounding_box = value

    def distance_to(self, position: Position) -> float:
        """Calculate the distance from the road to a given position."""
        if self.bounding_box.is_in(position):
            return 0.0

        min_distance = float('inf')
        for point in self.points:
            distance = math.sqrt((point.x - position.x) ** 2 + (point.y - position.y) ** 2 + (point.z - position.z) ** 2)
            if distance < min_distance:
                min_distance = distance

        return min_distance

    def json(self) -> dict:
        return {
            **super().json(),
            "hidden": self.hidden,
            "road_look": self.road_look.json(),
            "start_node_uid": self.start_node_uid,
            "end_node_uid": self.end_node_uid,
            "length": self.length,
            "maybe_divided": self.maybe_divided,
            # "points": [point.json() for point in self.points],
            # "lanes": [lane.json() for lane in self.lanes],
            # "bounding_box": self.bounding_box.json(),
            "railings": [railing.json() for railing in self.railings],
        }