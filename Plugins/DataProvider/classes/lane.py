from __future__ import annotations
from typing import Any, Literal, Optional

from Plugins.DataProvider.classes.node import Node

class Lane:
    forward: list[Optional[Lane]]
    """This is a list of lanes that can be reached by going forward on this one."""
    backward: list[Optional[Lane]]
    """This is a list of lanes that can be reached by going backward on this one."""
    left: Optional[Lane]
    """This is the lane to the left of this one."""
    right: Optional[Lane]
    """This is the lane to the right of this one."""
    
    forward_node: Node
    """This is the node that this lane is connected to when going forward."""
    backward_node: Node
    """This is the node that this lane is connected to when going backward."""