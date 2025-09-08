from typing import Literal


class NavigationNode:
    __slots__ = ["node_id", "distance", "direction", "is_one_lane_road"]

    node_id: str
    distance: float
    direction: Literal["forward", "backward"]
    is_one_lane_road: bool
    """This is a list of the lane indices that go through this navigation node."""

    def __init__(
        self,
        node_id: int | str,
        distance: float,
        direction: Literal["forward", "backward"],
        is_one_lane_road: bool,
    ):
        self.node_id = node_id
        self.distance = distance
        self.direction = direction
        self.is_one_lane_road = is_one_lane_road

    def json(self) -> dict:
        return {
            "node_id": self.node_id,
            "distance": self.distance,
            "direction": self.direction,
            "is_one_lane_road": self.is_one_lane_road,
        }


class NavigationEntry:
    __slots__ = ["uid", "forward", "backward"]

    uid: int | str
    forward: list[NavigationNode]
    backward: list[NavigationNode]

    def __init__(
        self,
        uid: int | str,
        forward: list[NavigationNode],
        backward: list[NavigationNode],
    ):
        self.uid = uid
        self.forward = forward
        self.backward = backward

    def json(self) -> dict:
        return {
            "uid": self.uid,
            "forward": [node.json() for node in self.forward],
            "backward": [node.json() for node in self.backward],
        }
