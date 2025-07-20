from __future__ import annotations
from typing import Any, Literal, Optional

from Plugins.DataProvider.classes.node import Node
from Plugins.DataProvider.classes.general import Transform, BoundingBox
from Plugins.DataProvider.classes.road import Road

class Lane:
    """
    All ETS2 data is parsed into this class. It's the central way to access lane data
    from the entire game. You should check the class definition for more information.
    """
    
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
    
    item_type: Literal["prefab", "road"]
    """Was this item originally a prefab or a road?"""
    item_uid: str
    """The unique ID of the item this lane belongs to."""
    
    lane_index: int
    """The index of the lane inside the current item."""
    lane_side: Optional[Literal["left", "right"]]
    """The side of the lane (left or right) inside the current item. Only available for roads."""
    
    semaphore_id: Optional[str]
    """Should this lane wait for a semaphore? If so this is the ID of that semaphore."""
    
    start: Transform
    """This is the start of the lane, used to generate points."""
    end: Transform
    """This is the end of the lane, used to generate points."""
    
    bounds: BoundingBox
    """The bounding box of this lane, used to check if a point is inside the lane."""