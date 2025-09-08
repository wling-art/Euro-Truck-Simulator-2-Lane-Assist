from __future__ import annotations
from typing import Literal, Optional

from Plugins.DataProvider.classes.node import Node
from Plugins.DataProvider.classes.general import Transform, BoundingBox
from Plugins.DataProvider.classes.road import Road
from Plugins.DataProvider.classes.prefab import Prefab


class LaneMarking:
    offset: float = 0.0
    """Positive = away, Negative = towards the center of the lane"""
    color: Literal["white", "yellow"] = "white"
    type: Literal["solid", "dashed", "dashed-short", "none"] = "solid"

    def __init__(
        self,
        offset: float = 0.0,
        type: Literal["solid", "dashed", "dashed-short", "none"] = "solid",
        color: Literal["white", "yellow"] = "white",
    ):
        self.offset = offset
        self.type = type
        self.color = color


class LaneMarkings:
    left: LaneMarking
    right: LaneMarking

    def __init__(self, left: LaneMarking, right: LaneMarking):
        self.left = left
        self.right = right


class LaneRailing:
    offset: float = 0.0
    """Positive = away, Negative = towards the center of the lane"""
    type: Literal["metal", "concrete", "pole", "none"] = "none"

    def __init__(
        self,
        offset: float = 0.0,
        type: Literal["metal", "concrete", "pole", "none"] = "none",
    ):
        self.offset = offset
        self.type = type


class LaneRailings:
    left: LaneRailing
    right: LaneRailing

    def __init__(self, left: LaneRailing, right: LaneRailing):
        self.left = left
        self.right = right


class LaneRule:
    speed_limit: float = 0.0
    at_start: Literal["yield", "stop", "none"] = "none"
    at_end: Literal["yield", "stop", "none"] = "none"

    def __init__(
        self,
        speed_limit: float = 0.0,
        at_start: Literal["yield", "stop", "none"] = "none",
        at_end: Literal["yield", "stop", "none"] = "none",
    ):
        self.speed_limit = speed_limit
        self.at_start = at_start
        self.at_end = at_end


class Lane:
    """
    All ETS2 data is parsed into this class. It's the central way to access lane data
    from the entire game. You should check the class definition for more information.
    """

    __slots__ = [
        "forward",
        "backward",
        "left",
        "right",
        "forward_node",
        "backward_node",
        "item",
        "item_type",
        "item_uid",
        "index",
        "side",
        "type",
        "markings",
        "railings",
        "rules",
        "semaphore_id",
        "start",
        "end",
        "bounds",
    ]

    forward: Optional[list[Lane]]
    """This is a list of lanes that can be reached by going forward on this one."""
    backward: Optional[list[Lane]]
    """This is a list of lanes that can be reached by going backward on this one."""
    left: Optional[Lane]
    """This is the lane to the left of this one."""
    right: Optional[Lane]
    """This is the lane to the right of this one."""

    forward_node: Node
    """This is the node that this lane is connected to when going forward."""
    backward_node: Node
    """This is the node that this lane is connected to when going backward."""

    item: Road | Prefab
    item_type: Literal["prefab", "road"]
    """Was this item originally a prefab or a road?"""
    item_uid: str
    """The unique ID of the item this lane belongs to."""

    index: int
    """The index of the lane inside the current item."""
    side: Optional[Literal["left", "right"]]
    """The side of the lane (left or right) inside the current item. Only available for roads."""
    type: Literal["normal", "rail", "dirt"]
    """The type of the lane."""
    markings: LaneMarkings
    """The lane markings for this lane."""
    railings: LaneRailings
    """The lane railings for this lane."""
    rules: LaneRule
    """The rules that apply to this lane."""

    semaphore_id: Optional[str]
    """Should this lane wait for a semaphore? If so this is the ID of that semaphore."""

    start: Transform
    """This is the start of the lane, used to generate points."""
    end: Transform
    """This is the end of the lane, used to generate points."""

    bounds: BoundingBox
    """The bounding box of this lane, used to check if a point is inside the lane."""

    def __init__(self):
        self.type = "normal"
        self.markings = LaneMarkings(LaneMarking(), LaneMarking())
        self.railings = LaneRailings(LaneRailing(), LaneRailing())
        self.rules = LaneRule()

    def __str__(self) -> str:
        text = f"Lane for {self.item_type} ({self.item_uid}) index={self.index}"
        if self.side:
            text += f" side={self.side}"
        if self.railings.left.type != "none" or self.railings.right.type != "none":
            text += f" left_rail={self.railings.left.type} right_rail={self.railings.right.type}"
        if self.markings.left.type != "none" or self.markings.right.type != "none":
            text += f" left_marking={self.markings.left.type} right_marking={self.markings.right.type}"
        return text
