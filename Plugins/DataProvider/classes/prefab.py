import math
from Plugins.DataProvider.classes.base_item import BaseItem, ItemType
from Plugins.DataProvider.classes.general import (
    SpawnPointType,
    Transform,
    Position,
    BoundingBox,
)
from Plugins.DataProvider.classes.map_points import RoadMapPoint, PolygonMapPoint
from typing import Literal


class PrefabNode:
    __slots__ = ["x", "y", "z", "rotation", "input_lanes", "output_lanes"]

    x: float
    y: float
    z: float
    rotation: float
    input_lanes: list[int]
    """indices into nav_curves"""
    output_lanes: list[int]
    """indices into nav_curves"""

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        rotation: float,
        input_lanes: list[int],
        output_lanes: list[int],
    ):
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation
        self.input_lanes = input_lanes
        self.output_lanes = output_lanes

    def json(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "rotation": self.rotation,
            "input_lanes": self.input_lanes,
            "output_lanes": self.output_lanes,
        }


class PrefabSpawnPoints:
    __slots__ = ["x", "y", "z", "type"]

    x: float
    y: float
    z: float
    type: SpawnPointType

    def __init__(self, x: float, y: float, z: float, type: SpawnPointType):
        self.x = x
        self.y = y
        self.z = z
        self.type = type

    def json(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z, "type": self.type}


class PrefabTriggerPoint:
    __slots__ = ["x", "y", "z", "action"]

    x: float
    y: float
    z: float
    action: str

    def __init__(self, x: float, y: float, z: float, action: str):
        self.x = x
        self.y = y
        self.z = z
        self.action = action

    def json(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z, "action": self.action}


class PrefabNavCurve:
    __slots__ = [
        "nav_node_index",
        "start",
        "end",
        "next_lines",
        "prev_lines",
        "semaphore_id",
        "_points",
    ]

    nav_node_index: int
    start: Transform
    end: Transform
    next_lines: list[int]
    prev_lines: list[int]
    semaphore_id: int
    _points: list[Position]

    def __init__(
        self,
        nav_node_index: int,
        start: Transform,
        end: Transform,
        next_lines: list[int],
        prev_lines: list[int],
        semaphore_id: int,
        points: list[Position],
    ):
        self.nav_node_index = nav_node_index
        self.start = start
        self.end = end
        self.next_lines = next_lines
        self.prev_lines = prev_lines
        self.semaphore_id = semaphore_id
        self._points = points

    @property
    def points(self) -> list[Position]:
        # if self._points == []:
        #     self._points = self.generate_points()
        return self._points

    @points.setter
    def points(self, value: list[Position]):
        self._points = value

    # def generate_points(self, road_quality: float = 1, min_quality: int = 4) -> list[Position]:
    #     new_points = []
    #
    #     # Data has Z as the height value, but we need Y
    #     sx = self.start.x
    #     sy = self.start.z
    #     sz = self.start.y
    #     ex = self.end.x
    #     ey = self.end.z
    #     ez = self.end.y
    #
    #     length = math.sqrt(math.pow(sx - ex, 2) + math.pow(sy - ey, 2) + math.pow(sz - ez, 2))
    #     radius = math.sqrt(math.pow(sx - ex, 2) + math.pow(sz - ez, 2))
    #
    #     tan_sx = math.cos((self.start.rotation)) * radius
    #     tan_ex = math.cos((self.end.rotation)) * radius
    #     tan_sz = math.sin((self.start.rotation)) * radius
    #     tan_ez = math.sin((self.end.rotation)) * radius
    #
    #     needed_points = int(length * road_quality)
    #     if needed_points < min_quality:
    #         needed_points = min_quality
    #     for i in range(needed_points):
    #         s = i / (needed_points - 1)
    #         x = math_helpers.Hermite(s, sx, ex, tan_sx, tan_ex)
    #         y = sy + (ey - sy) * s
    #         z = math_helpers.Hermite(s, sz, ez, tan_sz, tan_ez)
    #         new_points.append(Position(x, y, z))
    #
    #     return new_points
    #
    # def convert_to_relative(self, origin_node: Node, map_point_origin: PrefabNode):
    #     prefab_start_x = origin_node.x - map_point_origin.x
    #     prefab_start_y = origin_node.z - map_point_origin.z
    #     prefab_start_z = origin_node.y - map_point_origin.y
    #
    #     rot = float(origin_node.rotation - map_point_origin.rotation)
    #
    #     new_start_pos = math_helpers.RotateAroundPoint(self.start.x + prefab_start_x, self.start.z + prefab_start_z,
    #                                                    rot, origin_node.x, origin_node.y)
    #     new_start = Transform(new_start_pos[0], self.start.y + prefab_start_y, new_start_pos[1],
    #                           self.start.rotation + rot)
    #
    #     new_end_pos = math_helpers.RotateAroundPoint(self.end.x + prefab_start_x, self.end.z + prefab_start_z, rot,
    #                                                  origin_node.x, origin_node.y)
    #     new_end = Transform(new_end_pos[0], self.end.y + prefab_start_y, new_end_pos[1], self.end.rotation + rot)
    #
    #     new_points: list[Position] = []
    #     for point in self.points:
    #         new_point_pos = math_helpers.RotateAroundPoint(point.x + prefab_start_x, point.z + prefab_start_z, rot,
    #                                                        origin_node.x, origin_node.y)
    #         new_points.append(Position(new_point_pos[0], point.y + prefab_start_y, new_point_pos[1]))
    #
    #     return PrefabNavCurve(self.nav_node_index, new_start, new_end, self.next_lines, self.prev_lines, self.semaphore_id,
    #                           points=new_points)

    def json(self) -> dict:
        return {
            "nav_node_index": self.nav_node_index,
            "start": self.start.json(),
            "end": self.end.json(),
            "next_lines": self.next_lines,
            "prev_lines": self.prev_lines,
            "semaphore_id": self.semaphore_id,
            "points": [point.json() for point in self.points],
        }


class NavNodeConnection:
    __slots__ = ["target_nav_node_index", "curve_indeces"]

    target_nav_node_index: int
    curve_indeces: list[int]

    def __init__(self, target_nav_node_index: int, curve_indeces: list[int]):
        self.target_nav_node_index = target_nav_node_index
        self.curve_indeces = curve_indeces

    def json(self) -> dict:
        return {
            "target_nav_node_index": self.target_nav_node_index,
            "curve_indeces": self.curve_indeces,
        }


class PrefabNavNode:
    __slots__ = ["type", "end_index", "connections"]

    type: Literal["physical", "ai"]
    """
    **physical**: the index of the normal node (see nodes array) this navNode ends at.\n
    **ai**: the index of the AI curve this navNode ends at.
    """
    end_index: int
    connections: list[NavNodeConnection]

    def __init__(
        self,
        type: Literal["physical", "ai"],
        end_index: int,
        connections: list[NavNodeConnection],
    ):
        self.type = type
        self.end_index = end_index
        self.connections = connections

    def json(self) -> dict:
        return {
            "type": self.type,
            "end_index": self.end_index,
            "connections": [connection.json() for connection in self.connections],
        }


class PrefabNavRoute:
    __slots__ = ["curves", "distance", "_points", "prefab"]

    curves: list[PrefabNavCurve]
    distance: float
    _points: list[Position]

    def __init__(self, curves: list[PrefabNavCurve]):
        self.distance = 0
        self._points = []
        self.curves = curves
        self.prefab = None

    @property
    def points(self):
        if self._points == []:
            self._points = self.generate_points(prefab=self.prefab)
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    # def generate_points(self, prefab=None) -> list[Position]:
    #     self.prefab = prefab
    #
    #     new_points = []
    #     for curve in self.curves:
    #         new_points += curve.points
    #
    #     min_distance = 0.25
    #     last_point = new_points[0]
    #     accepted_points = [new_points[0]]
    #     for point in new_points:
    #         if math_helpers.DistanceBetweenPoints(point.tuple(), last_point.tuple()) > min_distance:
    #             accepted_points.append(point)
    #             last_point = point
    #
    #     new_points = accepted_points
    #
    #     distance = 0
    #     for i in range(len(new_points) - 1):
    #         distance += math.sqrt(
    #             math.pow(new_points[i].x - new_points[i + 1].x, 2) + math.pow(new_points[i].z - new_points[i + 1].z, 2))
    #     self.distance = distance
    #
    #     if type(prefab) == Prefab:
    #         start_node = None
    #         start_distance = math.inf
    #         end_node = None
    #         end_distance = math.inf
    #         for node in prefab.node_uids:
    #             node = data.map.get_node_by_uid(node)
    #             node_distance_start = math_helpers.DistanceBetweenPoints((node.x, node.y), (new_points[0].x, new_points[0].z))
    #             node_distance_end = math_helpers.DistanceBetweenPoints((node.x, node.y), (new_points[-1].x, new_points[-1].z))
    #
    #             if node_distance_start < start_distance:
    #                 start_distance = node_distance_start
    #                 start_node = node
    #             if node_distance_end < end_distance:
    #                 end_distance = node_distance_end
    #                 end_node = node
    #
    #         start_offset = 0
    #         end_offset = 0
    #
    #         if start_node is not None:
    #             start_offset = start_node.z - new_points[0].y
    #             if start_offset < 0.001 and start_offset > -0.001:
    #                 start_offset = 0
    #
    #         if end_node is not None:
    #             end_offset = end_node.z - new_points[-1].y
    #             if end_offset < 0.001 and end_offset > -0.001:
    #                 end_offset = 0
    #
    #         def interpolate_y(y1, y2, t):
    #             return y1 + (y2 - y1) * t
    #
    #         if start_offset != 0 or end_offset != 0:
    #             accepted_points = []
    #             for i, point in enumerate(new_points):
    #                 accepted_points.append(Position(point.x, point.y + interpolate_y(start_offset, end_offset, i / len(new_points)), point.z))
    #
    #             return accepted_points
    #
    #     return new_points

    # def generate_relative_curves(self, origin_node: Node, map_point_origin) -> list[PrefabNavCurve]:
    #     new_curves = []
    #     for curve in self.curves:
    #         new_curves.append(curve.convert_to_relative(origin_node, map_point_origin))
    #     return new_curves

    def json(self) -> dict:
        return {
            # "curves": [curve.json() for curve in self.curves],
            "points": [point.json() for point in self.points],
            "distance": self.distance,
        }


class Semaphore:
    __slots__ = ["x", "y", "z", "rotation", "type", "id"]
    x: float
    y: float
    z: float
    rotation: float
    type: str
    id: int

    def __init__(
        self, x: float, y: float, z: float, rotation: float, type: str, id: int
    ):
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation
        self.type = type
        self.id = id

    def json(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "rotation": self.rotation,
            "type": self.type,
            "id": self.id,
        }


class PrefabDescription:
    __slots__ = [
        "token",
        "nodes",
        "map_points",
        "spawn_points",
        "trigger_points",
        "nav_curves",
        "nav_nodes",
        "semaphores",
        "_nav_routes",
    ]

    token: str
    nodes: list[PrefabNode]
    map_points: list[RoadMapPoint | PolygonMapPoint]
    """Can also be PolygonMapPoint"""
    spawn_points: list[PrefabSpawnPoints]
    trigger_points: list[PrefabTriggerPoint]
    nav_curves: list[PrefabNavCurve]
    semaphores: list[Semaphore]
    _nav_routes: list[PrefabNavRoute]

    def __init__(
        self,
        token: str,
        nodes: list[PrefabNode],
        map_points: list[RoadMapPoint | PolygonMapPoint],
        spawn_points: list[PrefabSpawnPoints],
        trigger_points: list[PrefabTriggerPoint],
        nav_curves: list[PrefabNavCurve],
        semaphores: list[Semaphore] | None = None,
    ):
        self._nav_routes = []
        self.token = token
        self.nodes = nodes
        self.map_points = map_points
        self.spawn_points = spawn_points
        self.trigger_points = trigger_points
        self.nav_curves = nav_curves
        self.semaphores = semaphores if semaphores is not None else []

    @property
    def nav_routes(self) -> list[PrefabNavRoute]:
        # if self._nav_routes == []:
        #     self.build_nav_routes()

        return self._nav_routes

    @nav_routes.setter
    def nav_routes(self, value: list[PrefabNavRoute]):
        self._nav_routes = value

    # def build_nav_routes(self):
    #     starting_curves = prefab_helpers.find_starting_curves(self)
    #     self._nav_routes = []
    #     for curve in starting_curves:
    #         curve_routes = prefab_helpers.traverse_curve_till_end(curve, self)
    #         for route in curve_routes:
    #             nav_route = PrefabNavRoute(route)
    #             self._nav_routes.append(nav_route)

    def json(self) -> dict:
        return {
            "token": self.token,
            "nodes": [node.json() for node in self.nodes],
            "map_points": [point.json() for point in self.map_points],
            "spawn_points": [spawn.json() for spawn in self.spawn_points],
            "trigger_points": [trigger.json() for trigger in self.trigger_points],
            "nav_curves": [curve.json() for curve in self.nav_curves],
            "nav_routes": [route.json() for route in self.nav_routes],
            "semaphores": [semaphore.json() for semaphore in self.semaphores],
        }


class Prefab(BaseItem):
    __slots__ = [
        "hidden",
        "token",
        "node_uids",
        "origin_node_index",
        "type",
        "description",
        "z",
        "_nav_routes",
        "_bounding_box",
    ]

    hidden: bool
    token: str
    node_uids: list[str]
    origin_node_index: int
    type: ItemType
    description: PrefabDescription
    z: float
    _nav_routes: list[PrefabNavRoute]
    _bounding_box: BoundingBox

    def __init__(
        self,
        uid: str,
        x: float,
        y: float,
        z: float,
        hidden: bool | None,
        token: str,
        node_uids: list[str],
        origin_node_index: int,
    ):
        super().__init__(uid, ItemType.Prefab, x, y)
        self.type = ItemType.Prefab
        self.description = None
        self._nav_routes = []
        self._bounding_box = None
        self.z = z
        self.hidden = hidden
        self.token = token
        self.node_uids = node_uids
        self.origin_node_index = origin_node_index

    # def build_nav_routes(self):
    #     self._nav_routes = []
    #     for route in self.prefab_description.nav_routes:
    #         self._nav_routes.append(PrefabNavRoute(
    #             route.generate_relative_curves(data.map.get_node_by_uid(self.node_uids[0]),
    #                                            self.prefab_description.nodes[self.origin_node_index])
    #         ))
    #
    #     for route in self._nav_routes:
    #         route.generate_points(self)

    @property
    def nav_routes(self) -> list[PrefabNavRoute]:
        """The prefab description also has nav routes, but this nav route list has the correct world space positions."""
        # if self._nav_routes == []:
        #     self.build_nav_routes()

        return self._nav_routes

    @nav_routes.setter
    def nav_routes(self, value: list[PrefabNavRoute]):
        self._nav_routes = value

    @property
    def bounding_box(self) -> BoundingBox:
        if self._bounding_box is None:
            min_x = math.inf
            max_x = -math.inf
            min_y = math.inf
            max_y = -math.inf
            for route in self.nav_routes:
                for point in route.points:
                    if point.x < min_x:
                        min_x = point.x
                    if point.x > max_x:
                        max_x = point.x
                    if point.z < min_y:
                        min_y = point.z
                    if point.z > max_y:
                        max_y = point.z

            if min_x == math.inf:
                min_x = 0
            if max_x == -math.inf:
                max_x = 0
            if min_y == math.inf:
                min_y = 0
            if max_y == -math.inf:
                max_y = 0

            self._bounding_box = BoundingBox(min_x - 5, min_y - 5, max_x + 5, max_y + 5)

        return self._bounding_box

    @bounding_box.setter
    def bounding_box(self, value: BoundingBox):
        self._bounding_box = value

    def json(self) -> dict:
        return {
            **super().json(),
            "hidden": self.hidden,
            "token": self.token,
            "node_uids": [str(node) for node in self.node_uids],
            "origin_node_index": self.origin_node_index,
            # "origin_node": data.map.get_node_by_uid(self.node_uids[self.origin_node_index]).json(),
            "nav_routes": [route.json() for route in self.nav_routes],
            "bounding_box": self.bounding_box.json(),
            "description": self.description.json() if self.description else None,
        }
